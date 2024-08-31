from django.http import JsonResponse
import requests
import pandas as pd
from io import StringIO
import os

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
        "User-Agent": "Rendezvous-Radar" 
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

# Finds amenities near address
# Example url: http://127.0.0.1:8000/search-location/?address=Toronto&radius=10&experiences=family-friendly&activity=indoor,dining&audience=families,groups&seasons=summer,autumn,any&times=any
def find_poi(request):
    # Get parameters from query parameters
    faddr = request.GET.get('address')
    radius = request.GET.get('radius')
    experience = request.GET.get('experiences')
    activity = request.GET.get('activity')
    audience = request.GET.get('audience')
    season = request.GET.get('seasons')
    time = request.GET.get('times')

    if not faddr or not radius or not experience or not activity or not audience or not season or not time:
        return JsonResponse({'error': 'Parameter(s) are missing'}, status=400)
    
    # Splitting comma separated parameters into 
    experience_list = experience.split(',')
    activity_list = activity.split(',')
    audience_list = audience.split(',')
    season_list = season.split(',')
    time_list = time.split(',')

    # Geocoding endpoint
    url = f"https://nominatim.openstreetmap.org/search?q={faddr}&format=json"
    headers = {
        'referer': "https://jinhakimgh.github.io/Basketball-Court-Finder", # TODO: Change this
        "User-Agent": "Rendezvous-Radar" 
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
    
    # Retrieve coordinates from response
    lat, lon = data[0]["lat"], data[0]["lon"]

    query_dict = {
        'Experience': experience_list,
        'Activity_type': activity_list,
        'Audience': audience_list,
        'Season': season_list,  
        'Time': time_list
    }

    # Valid key-value pairs based on the query_dict
    valid_pairs = class_to_activity(query_dict)

    if len(valid_pairs) < 1:
        return JsonResponse({'error': 'No activities found.'}, status=400)
    

    # Creating the url and query to find the activities
    url = "https://overpass-api.de/api/interpreter"
    query = "[out:json];("

    for index in range(len(valid_pairs)):
        query += f'node(around:{radius},{lat},{lon})["{valid_pairs[index][0]}"="{valid_pairs[index][1]}"]["name"];'
                  
    
    query += ");out center;"

    params = {
        'data': query
    }

    # Make the second API call to find th elist of places
    try: 
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status() # Raise excetion for HTTP errors
        data = response.json()
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)
    except ValueError:
        return JsonResponse({'error': 'Invalid response format from API'}, status=500)

    # Adding the latitude and longitude to the response
    
    data["coordinates"] = {"lat": lat, "lon": lon}

    # Limits number of returned POIs
    if "elements" in data:
        data["elements"] = data["elements"][0:5] 

    poi_list = data.get("elements", [])
    
    for poi in poi_list:
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

    # Return the data as a JSON response
    return JsonResponse(data, safe=False)