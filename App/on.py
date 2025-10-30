import os
import pandas as pd

def first_existing(*paths):
	for p in paths:
		if os.path.exists(p):
			return p
	return None

scaled_candidates = [
	'/Users/lravi/Documents/project/res_app/data/features.csv',
	'/Users/lravi/Documents/project/res-app/data/features.csv',
	'./data/features.csv',
	'data/features.csv'
]

restaurant_candidates = [
	'/Users/lravi/Documents/project/res_app/data/restaurant_data.csv',
	'/Users/lravi/Documents/project/res-app/data/restaurant_data.csv',
	'./data/restaurant_data.csv',
	'data/restaurant_data.csv'
]

scaled_path = first_existing(*scaled_candidates)
if scaled_path is None:
	raise FileNotFoundError(
		"scaled.csv not found. Checked the following locations:\n" + "\n".join(scaled_candidates)
	)

restaurant_path = first_existing(*restaurant_candidates)
if restaurant_path is None:
	raise FileNotFoundError(
		"restaurant_data.csv not found. Checked the following locations:\n" + "\n".join(restaurant_candidates)
	)

# Load files (dfd and df are loaded from the same scaled file here; change if they should differ)
dfd = pd.read_csv(scaled_path)
df = pd.read_csv(scaled_path)

dfc = pd.read_csv(restaurant_path)

print("DataFrames loaded successfully.")

from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get database configuration with fallbacks
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Create connection URL with error handling
engine = create_engine(
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    
        
    # Save DataFrames to database
dfc.to_sql('restaurant_data', con=engine, if_exists='replace', index=False)
df.to_sql('features', con=engine, if_exists='replace', index=False)