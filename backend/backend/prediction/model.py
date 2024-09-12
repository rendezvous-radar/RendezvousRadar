import torch
from transformers import BertTokenizer, BertModel
from torch.nn import Module
from .bert_model import train_model


class MultiLabelBERTClassifier(Module):
    def __init__(self, num_labels):
        super(MultiLabelBERTClassifier, self).__init__()
        self.bert = BertModel.from_pretrained('bert-base-uncased')

        # Classification Head per category
        self.classifier_experience = torch.nn.Linear(self.bert.config.hidden_size, len(num_labels['experience']))
        self.classifier_activity = torch.nn.Linear(self.bert.config.hidden_size, len(num_labels['activity']))
        self.classifier_audience = torch.nn.Linear(self.bert.config.hidden_size, len(num_labels['audience']))
        self.classifier_time = torch.nn.Linear(self.bert.config.hidden_size, len(num_labels['time']))
        self.classifier_season = torch.nn.Linear(self.bert.config.hidden_size, len(num_labels['season']))

    def forward(self, input_ids, attention_mask):
        # Inputs passed through BERT
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        pooled_output = outputs[1]

        # Generate logits for each category
        logits_experience = self.classifier_experience(pooled_output)
        logits_activity = self.classifier_activity(pooled_output)
        logits_audience = self.classifier_audience(pooled_output)
        logits_time = self.classifier_time(pooled_output)
        logits_season = self.classifier_season(pooled_output)

        return logits_experience, logits_activity, logits_audience, logits_time, logits_season


# Categories and their classes
num_labels = {
    'experience': ['romantic', 'family-friendly', 'adventure', 'relaxation', 'cultural', 'educational', 'any'],
    'activity': ['outdoor', 'indoor', 'sports', 'dining', 'shopping', 'entertainment', 'any'],
    'audience': ['couples', 'families', 'groups', 'solo', 'any'],
    'time': ['morning', 'afternoon', 'evening', 'night', 'any'],
    'season': ['summer', 'winter', 'spring', 'autumn','any']
}

def load_model():
    try: 
        model = MultiLabelBERTClassifier(num_labels)
        model.load_state_dict(torch.load('backend/prediction/model.pth', map_location=torch.device('cpu')))
        model.eval()
        return model
    
    except Exception as e:
        train_model()

        # Retry loading model after training
        try: 
            model = MultiLabelBERTClassifier(num_labels)
            model.load_state_dict(torch.load('backend/prediction/model.pth', map_location=torch.device('cpu')))
            model.eval()
            return model
    
        except Exception as e:
            print(f"Failed to load the model again: {e}")
            return None

def predict(text):
    model = load_model()
    
    # Initializing BERT Tokenizer
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

    # Preprocess
    inputs = tokenizer(text, padding=True, truncation=True, return_tensors='pt', max_length=128)
    input_ids = inputs['input_ids']
    attention_mask = inputs['attention_mask']

    # Forward Pass
    with torch.no_grad():
        outputs = model(input_ids=input_ids, attention_mask=attention_mask)

    # Interpret the output
    # Assuming model output is a tuple of logits (one for each label category)
    experience_logits, activity_logits, audience_logits, time_logits, season_logits = outputs

    # Apply softmax to get probabilities
    experience_probs = torch.softmax(experience_logits, dim=1)
    activity_probs = torch.softmax(activity_logits, dim=1)
    audience_probs = torch.softmax(audience_logits, dim=1)
    time_probs = torch.softmax(time_logits, dim=1)
    season_probs = torch.softmax(season_logits, dim=1)

    # Convert probabilities to label predictions
    experience_pred = num_labels['experience'][experience_probs.argmax()]
    activity_pred = num_labels['activity'][activity_probs.argmax()]
    audience_pred = num_labels['audience'][audience_probs.argmax()]
    time_pred = num_labels['time'][time_probs.argmax()]
    season_pred = num_labels['season'][season_probs.argmax()]

    # Return the predictions
    return {
        'Experience': [experience_pred],
        'Activity_type': [activity_pred],
        'Audience': [audience_pred],
        'Time': [time_pred],
        'Season': [season_pred]
    }