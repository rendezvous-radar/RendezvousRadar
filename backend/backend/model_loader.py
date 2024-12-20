import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import pandas as pd

# Global variables to hold the model, tokenizer, and valid sequences
model = None
tokenizer = None
valid_activity_sequences = None
valid_activity_types = None

def load_model():
    global model, tokenizer, valid_activity_sequences, valid_activity_types

    if model is None or tokenizer is None:
        model_name = "jkim03/rendezvous-radar-model"
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Load model and tokenizer
        tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=True)
        model = AutoModelForCausalLM.from_pretrained(model_name, use_auth_token=True)
        model.to(device)

        # Load valid activity types
        csv_activities_path = "./activities.csv"
        df_activities = pd.read_csv(csv_activities_path)

        # Extract valid activity type column
        valid_activity_types = set(df_activities['Value'].dropna().unique())

        valid_activity_sequences = [
            tokenizer(activity, add_special_tokens=False).input_ids
            for activity in valid_activity_types
        ]

def get_model_tokenizer():
    if model is None or tokenizer is None:
        load_model()
    return model, tokenizer, valid_activity_sequences, valid_activity_types
