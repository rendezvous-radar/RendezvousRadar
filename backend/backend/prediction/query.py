import re
import requests
import time
from dotenv import load_dotenv
import os

def generate_response(model_id, prompt, valid_activity_types):
    num_beams, max_length = 5, 500

    # Load environment variables from environment file
    load_dotenv()

    api_url = f"https://api-inference.huggingface.co/models/{model_id}"
    headers = {"Authorization": f"Bearer {os.getenv('HUGGINGFACE_TOKEN')}"}

    # Prepare Payload for the API
    data = {
        "inputs": prompt,
        "parameters": {
            "max_length": max_length,
            "num_beams": num_beams,
            "early_stopping": True,
            "repetition_penalty": 3.0,
            "do_sample": True,
        },
    }


    while True:
        # Send Request to Hugging Face Inference API
        response = requests.post(api_url, headers=headers, json=data)

        if response.status_code == 503:
            print("Model is loading. Retrying...")
            time.sleep(response.json().get("estimated_time", 10))  # Wait for the estimated load time
        elif response.status_code == 200:
            break
        else:
            raise Exception(f"API Error: {response.status_code} - {response.json()}")
            
    # Decode the generated IDs into text
    generated_text = response.json()[0].get("generated_text", "")
    generated_text = generated_text[len(prompt):] # Removing prompt from generated_text
    generated_text = re.sub(r'[^a-zA-Z0-9, ]', '', generated_text)  # Remove bad characters

    corrections = {
        "archaeologicalsite": "archaeological_site",
        "swimming": "swimming_pool",
        "pool": "swimming_pool",
        "archaeological": "archaeological_site",
        "artscentre": "arts_centre",
        "arts": "arts_centre",
        "beachresort": "beach_resort",
        "bicyclerental": "bicycle_rental",
        "bicycle": "bicycle_rental",
        "campsite": "camp_site",
        "camp": "camp_site",
        "caveentrance": "cave_entrance",
        "cave": "cave_entrance",
        "communitycentre": "community_centre",
        "community": "community_centre",
        "golfcourse": "golf_course",
        "golf": "golf_course",
        "horseriding": "horse_riding",
        "horse": "horse_riding",
        "icecream": "ice_cream",
        "icerink": "ice_rink",
        "karaokebox": "karaoke_box",
        "karaoke": "karaoke_box",
        "miniaturegolf": "miniature_golf",
        "nationalpark": "national_park",
        "naturereserve": "nature_reserve",
        "picnicsite": "picnic_site",
        "picnic": "picnic_site",
        "placeofworship": "place_of_worship",
        "worship": "place_of_worship",
        "recreationground": "recreation_ground",
        "shoppingcentre": "shopping_centre",
        "shopping": "shopping_centre",
        "sportscentre": "sports_centre",
        "sports": "sports_centre",
        "swimmingpool": "swimming_pool",
        "swimming": "swimming_pool",
        "themepark": "theme_park",
        "warmemorial": "war_memorial",
        "waterpark": "water_park",
        "zipline": "zip_line"
    }

    all_keywords = set(valid_activity_types).union(corrections.keys())
    pattern = r'(' + '|'.join(map(re.escape, all_keywords)) + r')'

    matches = set(re.findall(pattern, generated_text.lower()))

    filtered_activities = [corrections.get(match, match) for match in matches]

    return filtered_activities

