from django.http import JsonResponse
import requests
from .model_loader import get_activities
from .prediction.query import generate_response
from .helper import class_to_activity, pairs_to_pois, extract_key_value_tuples
from huggingface_hub import InferenceApi

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

    valid_pairs = class_to_activity(query_dict)

    if len(valid_pairs) < 1:
        return JsonResponse({
            "message": "No valid activities were found for the given prompt.",
            "status": "no_valid_pairs",
            "elements": []
        }, status=200)

    return pairs_to_pois(valid_pairs, radius, lat, lon)

# Finds coordinates of an address
# Example: http://127.0.0.1:8000/find-coords/?address=Toronto
def findCoordinates(request):
    address = request.GET.get('address')

    if not address:
        return JsonResponse({'error': 'Address is missing'}, status=400)

    # Geocoding adrdress
    url = f"https://nominatim.openstreetmap.org/search?q={address}&format=json"
    headers = {
        'referer': "https://jinhakimgh.github.io/Basketball-Court-Finder",
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

def findFromPrompt(request):
    """
        Finds activities/POIs from a prompt.
        Calls the LLM model trained with distilgpt from InferenceAPI.
        Then processes data and calls Overpass API.
        Example url: http://127.0.0.1:8000/ai-search/?lat=43.6534817&lon=-79.3839347&radius=1000&prompt=Suggest+a+list+of+activities+for+a+romantic+date.
    """
    
    # Get parameters from query parameters
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')
    prompt = request.GET.get('prompt')
    radius = request.GET.get('radius')

    if not lat or not lon or not prompt or not radius:
        return JsonResponse({'error': 'Parameter(s) are missing'}, status=400)
    
    # Use inference api to retrieve data
    model_id = "jkim03/rendezvous-radar-model"

    # Load valid_activity_types
    valid_activity_types  = get_activities()

    # Returns prediction categorization from model
    preds = generate_response(model_id, prompt, valid_activity_types)
    
    key_val_list = extract_key_value_tuples("activities.csv", preds)

    return pairs_to_pois(key_val_list, radius, lat, lon)