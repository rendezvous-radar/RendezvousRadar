import pandas as pd
import requests
from django.http import JsonResponse

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

# Categorizes it with tags
def categorize_poi(poi):
    tags = poi.get('tags', {})

    category_map = {
        'food': [
            ('amenity', {'restaurant', 'cafe', 'fast_food', 'bar', 'pub', 'ice_cream'}),
            ('cuisine', None)
        ],
        'nature': [
            ('leisure', {'park', 'nature_reserve', 'garden', 'beach_resort', 'marina', 'recreation_ground'}),
            ('boundary', {'national_park'}),
            ('natural', None),
            ('place', {'island'}),
            ('tourism', {'picnic_site', 'viewpoint', 'camp_site'}),
            ('landuse', None),
            ('highway', {'path', 'track', 'trail'}),
            ('waterway', {'waterfall'})
        ],
        'shopping': [
            ('shop', None), 
            ('amenity', {'marketplace', 'pharmacy', 'convenience', 'retail'})
        ],
        'sports': [
            ('sport', None), 
            ('amenity', {'gym', 'bicycle_rental', 'dojo'}),
            ('leisure', {'sports_centre', 'stadium', 'pitch', 'swimming_pool', 'golf_course', 'fishing', 'horse_riding', 'miniature_golf', 'ice_rink', 'track'}),
            ('airway', {'zip_line'})
        ],
        'library': [
            ('amenity', {'library'})
        ],
        'entertainment': [
            ('amenity', {'arts_centre', 'cinema', 'karaoke_box', 'planetarium', 'sauna', 'theatre', }),
            ('leisure', {'playground', 'water_park'}),
            ('tourism', {'aquarium', 'attraction', 'theme_park', 'zoo'})
        ],
        'history': [
            ('historic', None),
            ('memorial', None)
        ]
    }

    for category, rules in category_map.items():
        for key, values in rules:
            if (values is None and key in tags) or (tags.get(key) is not None and tags.get(key) in values):
                return category
            
    # Uncategorized POI
    return 'uncategorized_poi'

def batch_list(lst, batch_size):
    """Helper function to split a list into batches. Max pairs is 30 to limit API calls"""
    for i in range(0, 30, batch_size):
        yield lst[i:i + batch_size]

def build_overpass_query(batch, radius, lat, lon, limit):
    """Build Overpass API query for a batch of valid pairs."""

    return "[out:json];(" + "".join(
        f'node(around:{radius},{lat},{lon})["{key.strip()}"="{value.strip()}"]["name"];'
        for key, value in batch
        ) + f");out {limit} center;"

def add_metadata_to_pois(pois):
    """Add address and category metadata to POIs."""
    for poi in pois:
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

            # Otherwise construct the address
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


def pairs_to_pois(valid_pairs, radius, lat, lon):
    if (len(valid_pairs) == 0): 
        return JsonResponse({
            "message": "No valid activities were found for the given prompt.",
            "status": "no_valid_pairs",
            "elements": []
        }, status=200)  # HTTP 200 OK since it's not an error, just no results

    batch_size = 20

    url = "https://overpass-api.de/api/interpreter"
    all_pois = []

    # Limits the amount of POIs returned per query
    max_per_lookup = 20

    for batch in batch_list(valid_pairs, batch_size):
        # Building query
        params = {'data': build_overpass_query(batch, radius, lat, lon, max_per_lookup)}

        headers = {
            'referer': "https://main.dud3dbh8mjohs.amplifyapp.com",
            "User-Agent": "Rendezvous-Radar",
        }

        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()

            if "elements" in data:
                for element in data["elements"]:
                    all_pois.append(element)
                
        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': str(e)}, status=500)
        except ValueError:
            return JsonResponse({'error': 'Invalid response format from API'}, status=500)

    # Adding the latitude and longitude to the response
    data = {"coordinates": {"lat": lat, "lon": lon}, "elements": all_pois}
    add_metadata_to_pois(data["elements"])
    
    # Return the data as a JSON response
    return JsonResponse(data, safe=False)

# Extracts key, value pairs from CSV file
def extract_key_value_tuples(csv_file, filter_values):
    # Read the CSV into a DataFrame
    df = pd.read_csv(csv_file)
    
    # Filter rows where 'Value' is in the filter_values list
    filtered_df = df[df['Value'].isin(filter_values)]
    
    # Extract the 'Key' and 'Value' columns as a list of tuples
    key_value_list = list(zip(filtered_df['Key'], filtered_df['Value']))
    
    return key_value_list