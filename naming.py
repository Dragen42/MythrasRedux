import pandas as pd
import random

def load_name_data(csv_file):
    df = pd.read_csv(csv_file)
    # Remove the first row which contains "Males" and "Females"
    df = df.iloc[1:]
    # Set the column names
    df.columns = ['Rank', 'Male_Name', 'Male_Number', 'Female_Name', 'Female_Number']
    return df

    
    
    
def get_random_male_name(df):
    if not isinstance(name_data, pd.DataFrame):
        raise ValueError("name_data must be a pandas DataFrame")

    male_names = name_data['Male_Name'].tolist()
    # Remove 'Name' from the list if it exists
    if 'Name' in male_names:
        male_names.remove('Name')
    return random.choice(male_names)

def get_random_female_name(df):
    if not isinstance(name_data, pd.DataFrame):
        raise ValueError("name_data must be a pandas DataFrame")

    female_names = name_data['Female_Name'].tolist()
    # Remove 'Name' from the list if it exists
    if 'Name' in female_names:
        female_names.remove('Name')
    return random.choice(female_names)

# Load the CSV file
csv_file = 'name_1940.csv'
name_data = load_name_data(csv_file)


