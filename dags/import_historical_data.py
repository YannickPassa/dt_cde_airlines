import os
from dotenv import load_dotenv
import zipfile
import pandas as pd
from kaggle.api.kaggle_api_extended import KaggleApi
from sqlalchemy import create_engine


load_dotenv()

# Set Kaggle credentials before importing Kaggle
os.environ['KAGGLE_USERNAME'] = os.getenv('KAGGLE_USERNAME')
os.environ['KAGGLE_KEY'] = os.getenv('KAGGLE_KEY')



def authenticate_kaggle_from_airflow():
    api = KaggleApi()
    api.authenticate()
    return api

def create_db_engine():
    """Create SQLAlchemy engine from environment variables."""
    host = os.getenv('PGHOST')
    user = os.getenv('PGUSER')
    password = os.getenv('PGPASSWORD')
    database = os.getenv('PGDATABASE')
    port = os.getenv('PGPORT')
    
    connection_string = f'postgresql://{user}:{password}@{host}:{port}/{database}'
    engine = create_engine(connection_string)
    
    return engine

def load_kaggle_dataset_to_dfs(api, dataset_name, file_names):
    """
    Load Kaggle dataset files directly into DataFrames.
    
    Args:
        api: Authenticated KaggleApi instance
        dataset_name: Dataset identifier (e.g., 'usdot/flight-delays')
        file_names: List of CSV file names to load
    
    Returns:
        dict: Dictionary with file names as keys and DataFrames as values
    """
    dataframes = {}
    
    for file_name in file_names:
        print(f"Loading {file_name}...")
        
        api.dataset_download_file(dataset_name, file_name, path='.', force=True, quiet=False)
        
        # The file might be zipped or not
        zip_name = f'{file_name}.zip'
        
        try:
            # Try to open as zip first
            if os.path.exists(zip_name):
                with zipfile.ZipFile(zip_name, 'r') as z:
                    with z.open(file_name) as f:
                        # Fix the dtype warning for flights.csv
                        dataframes[file_name.replace('.csv', '')] = pd.read_csv(f, low_memory=False)
                os.remove(zip_name)
            elif os.path.exists(file_name):
                # File is already unzipped
                dataframes[file_name.replace('.csv', '')] = pd.read_csv(file_name, low_memory=False)
                os.remove(file_name)
            else:
                print(f"Warning: Could not find {file_name} or {zip_name}")
        except Exception as e:
            print(f"Error loading {file_name}: {e}")
    
    return dataframes

# Authenticate Kaggle
api = authenticate_kaggle_from_airflow()

# Load datasets
dfs = load_kaggle_dataset_to_dfs(
    api,
    'usdot/flight-delays',
    ['flights.csv', 'airlines.csv', 'airports.csv']
)

flights_df = dfs['flights']
airlines_df = dfs['airlines']
airports_df = dfs['airports']

# Create engine
engine = create_db_engine()

# Import to database using connection context


airlines_df.to_sql('airlines', con=engine, if_exists='replace', index=False)

print("Import complete!")
