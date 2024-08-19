# -*- coding: utf-8 -*-
"""model_xgboost.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1H3UecROwadKXC7Bne995MplKj9sD4YW_
"""

#!pip install scikit-learn pandas xgboost

# Data Preparation
import pandas as pd

# Corrected expanded dataset without time_of_day and with equal array lengths
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
        'Top-rated vegan restaurants',
        'Find a cooking class happening tonight',
        'Late-night dessert spots',
        'Where to go for a fun group activity',
        'Suggest a family-friendly beach',
        'Looking for an educational workshop this weekend',
        'Where to find live music tonight',
        'Best coffee shops to work in the morning',
        'Where to find the best brunch spots',
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
        'Where to find the best donuts in town',
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
    'type_of_experience': [
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
    'activity_type': [
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
    'target_audience': [
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
    'seasonality': [
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
    'time_of_day': [
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

df = pd.DataFrame(data)

# Text Data -> Numerical Data TF-IDF.
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier
from sklearn.multioutput import MultiOutputClassifier

# Text Data -> Numerical Data TF-IDF with bi-grams
vectorizer = TfidfVectorizer(ngram_range=(1, 2))
X = vectorizer.fit_transform(df['text'])

# Encode Labels
label_encoders = {}
for column in ['type_of_experience', 'activity_type', 'target_audience', 'seasonality', 'time_of_day']:
    le = LabelEncoder()
    df[column] = le.fit_transform(df[column])
    label_encoders[column] = le

# Define and Train XGBoost Models
models = {}
for column in ['type_of_experience', 'activity_type', 'target_audience', 'seasonality', 'time_of_day']:
    clf = MultiOutputClassifier(XGBClassifier(eval_metric='mlogloss'))
    clf.fit(X, df[[column]])
    models[column] = clf

# Synonym Replacement Function
def preprocess_input(text):
    text = text.lower()
    text = text.replace("eat", "dine")
    text = text.replace("going out to eat", "dining")
    return text

# Predict on New Input
new_input = ["Where can I go out to eat with my family?"]
new_input = [preprocess_input(text) for text in new_input]
X_new = vectorizer.transform(new_input)

predictions = {}
for column in ['type_of_experience', 'activity_type', 'target_audience', 'seasonality', 'time_of_day']:
    pred = models[column].predict(X_new)
    predictions[column] = label_encoders[column].inverse_transform(pred[0])

# Print Predictions
for column, pred in predictions.items():
    print(f"{column.replace('_', ' ').title()}: {pred[0]}")