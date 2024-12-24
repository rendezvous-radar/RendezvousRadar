import pandas as pd

# Global variables to hold the valid activity types
valid_activity_types = None

def load_activities():
    global valid_activity_types

    if valid_activity_types is None:
       
        # Load valid activity types
        csv_activities_path = "./activities.csv"
        df_activities = pd.read_csv(csv_activities_path)

        # Extract valid activity type column
        valid_activity_types = set(df_activities['Value'].dropna().unique())

def get_activities():
    if valid_activity_types is None:
        load_activities()
    return valid_activity_types
