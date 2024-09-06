import torch
from transformers import BertTokenizer
from bert_model import MultiLabelBERTClassifier


def predict(text):

    # Categories and their classes
    num_labels = {
        'experience': ['romantic', 'family-friendly', 'adventure', 'relaxation', 'cultural', 'educational', 'any'],
        'activity': ['outdoor', 'indoor', 'sports', 'dining', 'shopping', 'entertainment', 'any'],
        'audience': ['couples', 'families', 'groups', 'solo', 'any'],
        'time': ['morning', 'afternoon', 'evening', 'night', 'any'],
        'season': ['summer', 'winter', 'spring', 'autumn','any']
    }

    # Define Model Class
    model = MultiLabelBERTClassifier(num_labels)
    model.load_state_dict(torch.load('model_state.pth'))
    model.eval()

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
        'experience': experience_pred,
        'activity': activity_pred,
        'audience': audience_pred,
        'time': time_pred,
        'season': season_pred
    }