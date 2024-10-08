import torch
from torch.utils.data import DataLoader, TensorDataset
from torch.optim import AdamW
from torch.nn import BCEWithLogitsLoss, Module
from transformers import BertTokenizer, BertModel, get_linear_schedule_with_warmup
import torch.nn.functional as F
import os

# Categories and their classes
num_labels = {
    'experience': ['romantic', 'family-friendly', 'adventure', 'relaxation', 'cultural', 'educational', 'any'],
    'activity': ['outdoor', 'indoor', 'sports', 'dining', 'shopping', 'entertainment', 'any'],
    'audience': ['couples', 'families', 'groups', 'solo', 'any'],
    'time': ['morning', 'afternoon', 'evening', 'night', 'any'],
    'season': ['summer', 'winter', 'spring', 'autumn','any']
}

# Initializing BERT Tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

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

# Data Preparation
data = {
    'text': [
        'Looking for date night food spots',
        'Where can I find a family-friendly restaurant?',
        'Suggest a romantic dinner place for the evening',
        'Best activities to do this weekend',
        'Where can I shop for new clothes?',
        'Find a cultural event happening this afternoon',
        'Looking for a quiet spot to relax this weekend',
        'Where can I take my family for a fun afternoon?',
        'Best nightclubs for dancing',
        'Top places for a romantic dinner',
        'Where to go for winter hiking',
        'Best beaches for summer',
        'Outdoor concerts this summer',
        'Cherry blossom viewing spots',
        'Top places to see fall foliage',
        'Where to find hot chocolate in winter',
        'Dog-friendly parks nearby',
        'Wheelchair-friendly hiking trails',
        'Accessible restaurants in the area',
        'Best places for an evening stroll',
        'Top-rated vegan spots to eat at',
        'Find a cooking class happening tonight',
        'Late-night dessert spots',
        'Where to go for a fun group activity',
        'Suggest a family-friendly beach',
        'Looking for an educational workshop this weekend',
        'Where to find live music tonight',
        'Best coffee shops to work in the morning',
        'Where to find the best brunch spots to eat at',
        'Suggest a good place for solo travel',
        'Top bars with live music',
        'Find a yoga retreat for relaxation',
        'Best shopping malls around',
        'Where to find the best flea markets',
        'Looking for a cultural experience this afternoon',
        'Where to take toddlers on a rainy day',
        'Suggest a place for team-building activities',
        'Best rooftop bars for dinner',
        'Find a pet-friendly hotel nearby',
        'Where to watch the sunset with a view',
        'Best places for a solo dinner',
        'Where to go for late-night shopping',
        'Looking for a place with great nightlife',
        'Best places to watch the sunrise',
        'Outdoor yoga classes near me',
        'Top golf courses in the area',
        'Best places to take kids on a weekend',
        'Where to take my dog for a walk',
        'Find a place to do indoor rock climbing',
        'Where to find the best donuts to eat in town',
        'Best beaches for surfing this summer',
        'Date spots in the area?',
        'Fun activities in our area?',
        'Historic spots in our area?',
        'Spots for a couple to visit?',
        'Where can I go out with my friends?',
        'Where can my date and I go out to?',
        'Best places to go eat?',
        'Places to eat near me',
        'Places to go eat with my family',
        'Good restaurants for dinner',
        'Family-friendly places to eat',
        'Romantic dining options',
        'Where to find the best food?',
        'Best places to eat in town'
    ],
    'experience': [
        'Romantic', 'Family-friendly', 'Romantic', 'Any', 'Shopping', 'Cultural',
        'Relaxation', 'Family-friendly', 'Nightlife', 'Romantic', 'Adventure', 'Relaxation',
        'Entertainment', 'Cultural', 'Cultural', 'Relaxation', 'Adventure', 'Relaxation',
        'Any', 'Relaxation', 'Any', 'Educational', 'Any', 'Entertainment',
        'Family-friendly', 'Educational', 'Nightlife', 'Any', 'Any', 'Adventure',
        'Nightlife', 'Relaxation', 'Shopping', 'Shopping', 'Cultural', 'Family-friendly',
        'Educational', 'Any', 'Relaxation', 'Romantic', 'Any', 'Shopping',
        'Nightlife', 'Relaxation', 'Outdoor', 'Sports', 'Family-friendly', 'Adventure',
        'Indoor', 'Any', 'Adventure', 'Romantic', 'Any', 'Cultural', 'Romantic', 'Any',
        'Romantic', 'Any', 'Any', 'Family-friendly', 'Any', 'Any', 'Any', 'Any', 'Any'
    ],
    'activity': [
        'Dining', 'Dining', 'Dining', 'Outdoor', 'Shopping', 'Entertainment',
        'Outdoor', 'Outdoor', 'Entertainment', 'Dining', 'Outdoor', 'Outdoor',
        'Entertainment', 'Outdoor', 'Outdoor', 'Dining', 'Outdoor', 'Outdoor',
        'Dining', 'Outdoor', 'Dining', 'Indoor', 'Dining', 'Entertainment',
        'Outdoor', 'Indoor', 'Entertainment', 'Dining', 'Dining', 'Outdoor',
        'Entertainment', 'Outdoor', 'Shopping', 'Shopping', 'Entertainment', 'Indoor',
        'Indoor', 'Dining', 'Outdoor', 'Outdoor', 'Dining', 'Shopping',
        'Entertainment', 'Outdoor', 'Outdoor', 'Sports', 'Outdoor', 'Outdoor',
        'Indoor', 'Dining', 'Outdoor', 'Any', 'Any', 'Any', 'Any', 'Any',
        'Any', 'Dining', 'Dining', 'Dining', 'Dining', 'Dining', 'Dining', 'Dining', 'Dining'
    ],
    'audience': [
        'Couples', 'Families', 'Couples', 'Groups', 'Solo', 'Groups',
        'Solo', 'Families', 'Groups', 'Couples', 'Solo', 'Solo',
        'Groups', 'Groups', 'Solo', 'Solo', 'Couples', 'Couples',
        'Solo', 'Couples', 'Couples', 'Groups', 'Couples', 'Groups',
        'Families', 'Groups', 'Couples', 'Solo', 'Solo', 'Solo',
        'Groups', 'Solo', 'Solo', 'Groups', 'Families', 'Groups',
        'Groups', 'Couples', 'Couples', 'Couples', 'Solo', 'Couples',
        'Groups', 'Solo', 'Solo', 'Families', 'Couples', 'Solo',
        'Couples', 'Couples', 'Couples', 'Couples', 'Any', 'Any', 'Any', 'Groups',
        'Couples', 'Any', 'Any', 'Families', 'Families', 'Families', 'Couples', 'Any', 'Any'
    ],
    'season': [
        'Any', 'Any', 'Any', 'Any', 'Any', 'Any',
        'Any', 'Any', 'Any', 'Any', 'Winter', 'Summer',
        'Summer', 'Spring', 'Autumn', 'Winter', 'Any', 'Any',
        'Any', 'Any', 'Any', 'Any', 'Any', 'Any',
        'Any', 'Any', 'Any', 'Any', 'Any', 'Any',
        'Any', 'Any', 'Any', 'Any', 'Any', 'Any',
        'Any', 'Any', 'Any', 'Any', 'Any', 'Any',
        'Any', 'Any', 'Any', 'Any', 'Any', 'Any', 'Any', 'Any', 'Any', 'Any',
        'Any', 'Any', 'Any', 'Any', 'Any', 'Any', 'Any', 'Any', 'Any', 'Any', 'Any', 'Any', 'Any'
    ],
    'time': [
        'Night', 'Any', 'Evening', 'Any', 'Any', 'Afternoon',
        'Any', 'Afternoon', 'Night', 'Evening', 'Any', 'Any',
        'Evening', 'Morning', 'Any', 'Any', 'Any', 'Any',
        'Evening', 'Any', 'Evening', 'Night', 'Night', 'Any',
        'Any', 'Any', 'Night', 'Morning', 'Morning', 'Any',
        'Night', 'Any', 'Any', 'Afternoon', 'Any', 'Any',
        'Any', 'Evening', 'Evening', 'Evening', 'Night', 'Night',
        'Morning', 'Any', 'Any', 'Any', 'Any', 'Any',
        'Any', 'Morning', 'Any', 'Any', 'Any', 'Any', 'Any', 'Any', 'Any', 'Any',
        'Any', 'Any', 'Evening', 'Any', 'Evening', 'Any', 'Any'
    ]
}

def one_hot_encode(label, category):
    # Convert label to OHE vector based on category
    vector = [0] * len(num_labels[category])
    if label in num_labels[category]:
      vector[num_labels[category].index(label)] = 1

    return vector

def train_model():
    encoded_data = {
        'text': data['text'],
        'experience': [one_hot_encode(label.lower(), 'experience') for label in data['experience']],
        'activity': [one_hot_encode(label.lower(), 'activity') for label in data['activity']],
        'audience': [one_hot_encode(label.lower(), 'audience') for label in data['audience']],
        'season': [one_hot_encode(label.lower(), 'season') for label in data['season']],
        'time': [one_hot_encode(label.lower(), 'time') for label in data['time']]
    }

    # Tokenize the text data
    inputs = tokenizer(encoded_data['text'], padding=True, truncation=True, return_tensors="pt", max_length=128)

    # Convert labels to tensors
    labels_experience = torch.tensor(encoded_data['experience'], dtype=torch.float32)
    labels_activity = torch.tensor(encoded_data['activity'], dtype=torch.float32)
    labels_audience = torch.tensor(encoded_data['audience'], dtype=torch.float32)
    labels_time = torch.tensor(encoded_data['time'], dtype=torch.float32)
    labels_season = torch.tensor(encoded_data['season'], dtype=torch.float32)

    # Create a DataLoader
    dataset = TensorDataset(
        inputs['input_ids'],
        inputs['attention_mask'],
        labels_experience,
        labels_activity,
        labels_audience,
        labels_time,
        labels_season
    )
    dataloader = DataLoader(dataset, batch_size=2, shuffle=True)

    # Hyperparameters
    learning_rate = 5e-5
    num_epochs = 4
    warmup_steps = 0
    weight_decay = 0.1
    max_grad_norm = 1.0

    # Initialize model
    model = MultiLabelBERTClassifier(num_labels)
    optimizer = AdamW(model.parameters(), lr=learning_rate, weight_decay=weight_decay)

    # Create a learning rate scheduler
    total_steps = len(dataloader) * num_epochs
    scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps=warmup_steps, num_training_steps=total_steps)

    model.train()

    loss_fn = BCEWithLogitsLoss()

    # Training loop
    for epoch in range(num_epochs):
        epoch_loss = 0
        for batch in dataloader:
            input_ids, attention_mask, labels_experience, labels_activity, labels_audience, labels_time, labels_season = batch

            optimizer.zero_grad()

            # Forward Pass
            logits_experience, logits_activity, logits_audience, logits_time, logits_season = model(input_ids, attention_mask)

            # Calculate Loss
            loss_experience = loss_fn(logits_experience, labels_experience)
            loss_activity = loss_fn(logits_activity, labels_activity)
            loss_audience = loss_fn(logits_audience, labels_audience)
            loss_time = loss_fn(logits_time, labels_time)
            loss_season = loss_fn(logits_season, labels_season)

            # Total Loss
            loss = loss_experience + loss_activity + loss_audience + loss_time + loss_season
            loss.backward()

            # Gradient clipping
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_grad_norm)

            optimizer.step()
            scheduler.step()

            epoch_loss += loss.item()

        avg_epoch_loss = epoch_loss / len(dataloader)
        print(f'Epoch {epoch + 1}, Average Loss: {avg_epoch_loss:.4f}')

    # Evaluation
    model.eval()

    # Saving the model
    save_dir = 'backend/prediction/' 
    save_path = os.path.join(save_dir, 'model.pth')
    torch.save(model.state_dict(), save_path)