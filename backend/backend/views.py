from django.http import JsonResponse
import requests
import pandas as pd
from io import StringIO
import os
from .prediction.model import predict

# Object of inputted classifications
def class_to_activity(classifications):
    df = pd.read_csv("./activities.csv")

    def activity_matches(row, preds):

        # Check each category in the row
        for category, class_list in preds.items():
            if 'any' in class_list:
                continue # Don't match if any

            # Get the row's classifications for the current category
            row_classifications = set(row[category].lower().split(', ')) if pd.notna(row[category]) else set()
            
            # Check if there's a match, considering blank categories
            if row_classifications and not all(pred.lower() in row_classifications for pred in class_list):
                return False
            
        return True

    # Apply the matching function to each row
    matching_activities = df[df.apply(activity_matches, axis=1, args=(classifications,))]

    # Return the key-value pairs of matching activities
    return [(row['Key'], row['Value']) for _, row in matching_activities.iterrows()]

def geocodeapi(lat, lon):
    url = f"https://nominatim.openstreetmap.org/reverse?format=geojson&lat={lat}&lon={lon}"

    headers = {
        'referer': "https://jinhakimgh.github.io/Basketball-Court-Finder", # TODO: Change this
        "User-Agent": "Rendezvous-Radar",
    }

    # Make the API call
    try: 
        response = requests.get(url, headers=headers)
        response.raise_for_status() # Raise excetion for HTTP errors
        data = response.json()
    except requests.exceptions.RequestException as e:
        return ""
    except ValueError:
        return ""
    
    address = data.get("features", [])[0].get("properties", {}).get("address", {})

    if address.get('house_number') and address.get('road'):
        first_part = f"{address.get('house_number', '')} {address.get('road', '')}"
    else:
        first_part = address.get('house_number', '') or address.get('road', '')
    

    address_parts = [
        first_part,
        address.get('city', ''),
        address.get('state', ''),
        address.get('postcode', '')
    ]

    address_parts = [part for part in address_parts if part]

    return ", ".join(address_parts)

def categorize_poi(poi):
    tags = poi.get('tags', {})

    # Food Category
    if tags.get('amenity') in ['restaurant', 'cafe', 'fast_food', 'bar', 'pub', 'ice_cream'] or 'cuisine' in tags:
        return 'food'
    
    # Nature category
    if tags.get('leisure') in ['park', 'nature_reserve', 'garden'] or \
       tags.get('natural') in ['wood', 'water', 'tree'] or \
       tags.get('tourism') in ['picnic_site', 'viewpoint'] or \
       tags.get('landuse') == 'forest':
        return 'nature'
    
    # Shopping category
    if 'shop' in tags or tags.get('amenity') in ['marketplace', 'pharmacy', 'convenience', 'retail']:
        return 'shopping'
    
    # Sports category
    if tags.get('leisure') in ['sports_centre', 'fitness_centre', 'stadium', 'pitch', 'swimming_pool', 'bowling_alley'] or \
       'sport' in tags:
        return 'sports'
    
    # Uncategorized POI
    return 'uncategorized_poi'

# Helper function to split a list into batches.
def batch_list(lst, batch_size):
    for i in range(0, len(lst), batch_size):
        yield lst[i:i + batch_size]

def pairs_to_pois(query_dict, radius, lat, lon):
    # Valid key-value pairs based on the query_dict
    valid_pairs = class_to_activity(query_dict)

    if len(valid_pairs) < 1:
        return JsonResponse({'error': 'No activities found.'}, status=400)
    

    batch_size = 10

    url = "https://overpass-api.de/api/interpreter"
    all_pois = []

    for batch in batch_list(valid_pairs, batch_size):
        # Creating the query for each batch
        query = "[out:json];("
        for pair in batch:
            key, value = pair[0].strip(), pair[1].strip()  # Stripping any extra spaces
            query += f'node(around:{radius},{lat},{lon})["{key}"="{value}"]["name"];'
        query += ");out center;"

        params = {'data': query}

        headers = {
            'referer': "https://jinhakimgh.github.io/Basketball-Court-Finder",  # TODO: Change this
            "User-Agent": "Rendezvous-Radar",

        }

        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()

            if "elements" in data:
                all_pois.extend(data["elements"])

        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': str(e)}, status=500)
        except ValueError:
            return JsonResponse({'error': 'Invalid response format from API'}, status=500)

    # Adding the latitude and longitude to the response
    data = {"coordinates": {"lat": lat, "lon": lon}, "elements": all_pois}

    # Limits number of returned POIs
    data["elements"] = data["elements"][0:(int(radius) // 20) - 1] 

    
    for poi in data["elements"]:
        # Add address to each POI and add overall category for markers (food, nature, shopping, sports, uncategorized_poi)
        if "tags" in poi:
            address = ""
            addr_city = poi["tags"].get("addr:city", "")
            addr_housenumber = poi["tags"].get("addr:housenumber", "")
            addr_postcode = poi["tags"].get("addr:postcode", "")
            addr_street = poi["tags"].get("addr:street", "")
            addr_state = poi["tags"].get("addr:state", "")

            # If house number or street is missing, query the API
            if not addr_housenumber or not addr_street:
                address = geocodeapi(poi.get("lat", 0), poi.get("lon", 0))

            else:

                address_parts = [
                    addr_housenumber + " " + addr_street,
                    addr_city,
                    addr_state,
                    addr_postcode
                ]

                address_parts = [part for part in address_parts if part]

                address = ", ".join(address_parts)

            poi["tags"]["address"] = address

            poi["tags"]["category"] = categorize_poi(poi)

    # Return the data as a JSON response
    return JsonResponse(data, safe=False)

# Finds amenities near address
# Example url: http://127.0.0.1:8000/search-location/?lat=43.6534817&lon=-79.3839347&radius=1000&experiences=family-friendly&activity=indoor,dining&audience=families,groups&seasons=summer,autumn,any&times=any
def find_poi(request):
    # Get parameters from query parameters
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')
    radius = request.GET.get('radius')
    experience = request.GET.get('experiences')
    activity = request.GET.get('activity')
    audience = request.GET.get('audience')
    season = request.GET.get('seasons')
    time = request.GET.get('times')

    if not lat or not lon or not radius or not experience or not activity or not audience or not season or not time:
        return JsonResponse({'error': 'Parameter(s) are missing'}, status=400)
    
    # Splitting comma separated parameters into 
    experience_list = experience.split(',')

    activity_list = activity.split(',')
    audience_list = audience.split(',')
    season_list = season.split(',')
    time_list = time.split(',')

    query_dict = {
        'Experience': experience_list,
        'Activity_type': activity_list,
        'Audience': audience_list,
        'Season': season_list,  
        'Time': time_list
    }

    return pairs_to_pois(query_dict, radius, lat, lon)

# Finds coordinates of an address
# Example: http://127.0.0.1:8000/find-coords/?address=Toronto
def findCoordinates(request):
    address = request.GET.get('address')

    if not address:
        return JsonResponse({'error': 'Address is missing'}, status=400)

    # Geocoding adrdress
    url = f"https://nominatim.openstreetmap.org/search?q={address}&format=json"
    headers = {
        'referer': "https://jinhakimgh.github.io/Basketball-Court-Finder", # TODO: Change this
        "User-Agent": "Rendezvous-Radar",
    }

    # Make the API call
    try: 
        response = requests.get(url, headers=headers)
        response.raise_for_status() # Raise excetion for HTTP errors
        data = response.json()
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)
    except ValueError:
        return JsonResponse({'error': 'Invalid response format from API'}, status=500)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()  # Parse the JSON response
    else:
        return JsonResponse({'error': 'Failed to fetch data from the external API'}, status=500)

    # Check if request returns at least one location
    if len(data) < 1 :
        return JsonResponse({'error': 'No locations found.'}, status=500)

    if "lat" not in data[0] or "lon" not in data[0]:
        return JsonResponse({'error': 'Error in API response formatting.'}, status=500)
    
    data = {"lat": data[0]["lat"], "lon": data[0]["lon"]}

    # Return data
    return JsonResponse(data)

# Finds amenities from prompt
def findFromPrompt(request):
    # Get parameters from query parameters
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')
    prompt = request.GET.get('prompt')
    radius = request.GET.get('radius')

    if not lat or not lon or not prompt:
        return JsonResponse({'error': 'Parameter(s) are missing'}, status=400)
    
    # Returns prediction categorization from model
    preds = predict(prompt)

    return pairs_to_pois(preds, radius, lat, lon)