from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments
import torch
from datasets import Dataset
import pandas as pd
import os
import re
from CustomLogitsProcessor import ConstrainLogitsProcessor


os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Load valid activity types
csv_activities_path = "./activities.csv"
df_activities = pd.read_csv(csv_activities_path)

# Extract valid activity type column
valid_activity_types = set(df_activities['Value'].dropna().unique())

# Load CSV into Pandas DF
csv_prompt_path = "prompt_training.csv"
df_prompt = pd.read_csv(csv_prompt_path)
print(df_prompt.head())

# Convert DF into Hugging Face DF
dataset = Dataset.from_pandas(df_prompt)

# Load pre-trained model and tokenizer from Hugging Face
model_name = "distilgpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token # Set pad token to EOS token
valid_activity_sequences = [
    tokenizer(activity, add_special_tokens=False).input_ids
    for activity in valid_activity_types
]

# Set the device to CPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = AutoModelForCausalLM.from_pretrained(model_name)
model.to(device)

# Preprocesses the data and returns labels
def preprocess(examples):
    # Concat prompt and completion with separator
    inputs = [prompt + "\n" + completion for prompt, completion in zip(examples['Prompt'], examples['Completion']) if prompt and completion]

    # Tokenize inputs
    encoding = tokenizer(inputs, truncation=True, padding="max_length", max_length=512)

    # Add the labels to the encoding
    encoding['labels'] = [
        [label if label != tokenizer.pad_token_id else -100 for label in input_id]
        for input_id in encoding['input_ids']
    ]


    return encoding # Ensure all return values are lists

# Preprocess the dataset
tokenized_dataset = dataset.map(preprocess, batched=True)

# Training Arguments
training_args = TrainingArguments(
    output_dir="./results",              # output dir
    num_train_epochs=8,                  # number of training epochs
    per_device_train_batch_size=2,       # batch size / device
    logging_dir="./logs",                # logs dir
    logging_steps=10,                    # steps/log
    save_steps=50,                      # steps/save
    warmup_steps=100,                    
    weight_decay=0.01,
    learning_rate=5e-4                
)

# Initialize the Trainer
trainer = Trainer(
    model=model,                          # Distilgpt2 model
    args=training_args,                   # training arguments
    train_dataset=tokenized_dataset      # training dataset
)

# Start training
trainer.train()

# Set the model to evaluation mode and disable gradient calculations for inference
model.eval()
torch.no_grad()

# Function to filter and generate results
def generate_filtered_output(prompt, num_beams, max_length=200):
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
    print(f"Generated Text: {generated_text}")

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

    filtered_activities = []
    for activity in activity_list:
        if activity in valid_activity_types:
            filtered_activities.append(activity)

        elif activity in corrections:
            filtered_activities.append(corrections[activity])
    
    # Return the filtered activities as a list
    return filtered_activities

model.to(device)

# Example prompt and output
prompt = "Suggest a list of activities for a romantic date."
output = set(generate_filtered_output(prompt, num_beams=5, max_length=500))
print("Generated Output:", output)

prompt = "Suggest fun activities for the day."
output = set(generate_filtered_output(prompt, num_beams=5, max_length=500))
print("Generated Output:", output)

prompt = "Soccer fields nearby."
output = set(generate_filtered_output(prompt, num_beams=5, max_length=500))
print("Generated Output:", output)

prompt = "Where can I play basketball"
output = set(generate_filtered_output(prompt, num_beams=5, max_length=500))
print("Generated Output:", output)

# Push model and tokenizer to Hugging Face Hub
# trainer.save_model("./updated_model")
# model.push_to_hub("jkim03/rendezvous-radar-model", force=True)
# tokenizer.push_to_hub("jkim03/rendezvous-radar-model", force=True)