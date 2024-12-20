import torch
from .CustomLogitsProcessor import ConstrainLogitsProcessor
import re

def generate_response(model, prompt, tokenizer, valid_activity_sequences, valid_activity_types):
    num_beams, max_length = 5, 500

    # Tokenize the input prompt
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, padding=True)

    logits_processor = ConstrainLogitsProcessor(valid_activity_sequences)

    attention_mask = inputs.get('attention_mask', None)

    # Set pad_token_id explicitly to eos_token_id to prevent EOS interference
    model.config.pad_token_id = model.config.eos_token_id

    # Generate text 
    with torch.no_grad():
        generated_ids = model.generate(
            input_ids = inputs['input_ids'], 
            max_length=max_length, 
            num_beams=num_beams, 
            early_stopping=True,
            repetition_penalty=3.0,
            attention_mask=attention_mask,
            pad_token_id=model.config.pad_token_id,
            do_sample=True,
            logits_processor=[logits_processor]
        )
    
    # Decode the generated IDs into text
    generated_text = tokenizer.decode(generated_ids[0], skip_special_tokens=True)[len(prompt):] # Removing prompt from generated_text
    generated_text = re.sub(r'[^a-zA-Z0-9, ]', '', generated_text)  # Remove bad characters

    # Split the generated text by commas and filter out invalid activities
    activity_list = [activity.strip() for activity in generated_text.split(',')]

    # correcting multi-word values
    corrections = {
        "archaeologicalsite": "archaeological_site",
        "artscentre": "arts_centre",
        "beachresort": "beach_resort",
        "bicyclerental": "bicycle_rental",
        "campsite": "camp_site",
        "caveentrance": "cave_entrance",
        "communitycentre": "community_centre",
        "golfcourse": "golf_course",
        "horseriding": "horse_riding",
        "icecream": "ice_cream",
        "icerink": "ice_rink",
        "karaokebox": "karaoke_box",
        "miniaturegolf": "miniature_golf",
        "nationalpark": "national_park",
        "naturereserve": "nature_reserve",
        "picnicsite": "picnic_site",
        "placeofworship": "place_of_worship",
        "recreationground": "reacreation_ground",
        "shoppingcentre": "shopping_centre",
        "sportscentre": "sports_centre",
        "swimmingpool": "swimming_pool",
        "themepark": "theme_park",
        "warmemorial": "war_memorial",
        "waterpark": "water_park",
        "zipline": "zip_line"
    }

    filtered_activities = set()
    for activity in activity_list:
        if activity in filtered_activities:
            continue
        
        if activity in valid_activity_types:
            filtered_activities.add(activity)

        elif activity in corrections:
            filtered_activities.add(corrections[activity])
    
    # Return the filtered activities as a list
    return filtered_activities

