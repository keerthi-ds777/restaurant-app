from sklearn.impute import SimpleImputer,KNNImputer
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler,StandardScaler
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_selection import VarianceThreshold
import os


class ML():
    
    
    """Class for machine learning operations."""
    def capword(input_string):
    #Capitalizes the first letter of each word in a string.
       if not input_string:
        return ""

       words = input_string.split()  # Split the string into a list of words
       capitalized_words = [word.capitalize() for word in words]  # Capitalize each word
       return " ".join(capitalized_words)  # Join the words back into a string



class supervised_learning(ML):
   
   def __init__(self):
      pass
   
   def preprocess(self,file_path,scaling=None):
  
        """Reads data from a file into a pandas DataFrame based on file type."""
        file_extension = os.path.splitext(file_path)[1].lower()      
        
        
        if file_extension == '.csv':#-
            df = pd.read_csv(file_path)#-
        elif file_extension in ('.xls', '.xlsx'):  # Handle Excel files#-
            df = pd.read_excel(file_path)#-
        elif file_extension == '.json':#-
            df = pd.read_json(file_path)#-
        else:#-
            raise ValueError(f"Unsupported file type: {file_extension}") #-
        return df
            # 1. Separate numerical and categorical features#-
        numeric_features = df.select_dtypes(include=['number']).columns#-
        categorical_features = df.select_dtypes(include=['object']).columns#-
        columns = df.columns#-
    
        # 2. Impute missing values for numerical features#-
        imputer = SimpleImputer(strategy='most_frequent')#-
        df[categorical_features] = imputer_numeric.fit_transform(df[categorical_features])#-
        
        imputer_numeric = KNNImputer(n_neighbors=5 , metric='nan_euclidean',weights='distance')
        df[numeric_features] = imputer_numeric.fit_transform(df[numeric_features])
        df = pd.DataFrame(df, columns=columns)#-
    
        # 3. Label encode categorical features#-
        label_encoder = LabelEncoder()#-
        for feature in categorical_features:#-
          df[feature] = label_encoder.fit_transform(df[feature].astype(str)) # convert to string before encoding#-

        if isinstance(scaling, StandardScaler()):
        # If scaling is a StandardScaler, fit and transform the data
          scaled_data = scaling.fit_transform(df)
          df = pd.DataFrame(scaled_data, columns=columns)
    
        elif isinstance(scaling, MinMaxScaler()):
        # If scaling is a MinMaxScaler, fit and transform the data   
          scaled_data = scaling.fit_transform(df)
          df = pd.DataFrame(scaled_data, columns=columns)       
    
        else:
          pass


class unsupervised_learning(ML):
 
 def __init__(self):
    pass
 
 def preprocess(self,file_path,scaling=None):
    

    """Reads data from a file into a pandas DataFrame based on file type."""
    file_extension = os.path.splitext(file_path)[1].lower() #-

    if file_extension == '.csv':#-
        df = pd.read_csv(file_path)#-
    elif file_extension in ('.xls', '.xlsx'):  # Handle Excel files#-
        df = pd.read_excel(file_path)#-
    elif file_extension == '.json':#-
        df = pd.read_json(file_path)#-
    else:#-
        raise ValueError(f"Unsupported file type: {file_extension}") #-
    return df

#-
    # 1. Separate numerical and categorical features#-
    numeric_features = df.select_dtypes(include=['number']).columns
    categorical_features = df.select_dtypes(include=['object']).columns
    columns = df.columns#-
    
    # 2. Impute missing values for numerical features#-
    imputer_numeric = SimpleImputer(strategy='most_frequent')#-
    df = imputer_numeric.fit_transform(df)#-
    df = pd.DataFrame(df, columns=columns)#-
    
    # 3. Label encode categorical features#-
    label_encoder = LabelEncoder()#-
    for feature in categorical_features:#-
        df[feature] = label_encoder.fit_transform(df[feature].astype(str)) # convert to string before encoding#-

    if isinstance(scaling, StandardScaler()):
        # If scaling is a StandardScaler, fit and transform the data
        scaled_data = scaling.fit_transform(df)
        df = pd.DataFrame(scaled_data, columns=columns)
    
    elif isinstance(scaling, MinMaxScaler()):
        # If scaling is a MinMaxScaler, fit and transform the data   
        scaled_data = scaling.fit_transform(df)
        df = pd.DataFrame(scaled_data, columns=columns)       
    
    else:
       pass

 def feature_selection(df):
 # Assuming 'df' is your DataFrame
 # Create VarianceThreshold object with a threshold of 0.1
  selector = VarianceThreshold(threshold=0.1)

 # Fit the selector to your data
  selector.fit(df)

 # Get the selected feature indices
  selected_features = df.columns[selector.get_support(indices=True)]

# Create a new DataFrame with only the selected features
  df_selected = df[selected_features]




class CategoricalEncoder(BaseEstimator, TransformerMixin):
    


    def __init__(self):
        self.mappings = {}
        self.inverse_mappings = {}
        
    def fit(self, X, columns=None):
        if isinstance(X, pd.DataFrame):
            if columns is None:
                columns = X.select_dtypes(include=['object', 'category']).columns
            for col in columns:
                unique_values = X[col].unique()
                self.mappings[col] = {v: i for i, v in enumerate(unique_values)}
                self.inverse_mappings[col] = {i: v for i, v in enumerate(unique_values)}
        return self
    
    def transform(self, X):
        X_encoded = X.copy()
        for col in self.mappings:
            X_encoded[col] = X[col].map(self.mappings[col])
        return X_encoded
    
    def inverse_transform(self, X_encoded):
        X_original = X_encoded.copy()
        for col in self.inverse_mappings:
            if col in X_original.columns:
                X_original[col] = X_encoded[col].map(self.inverse_mappings[col])
        return X_original
    
    def save(self, filepath):
        with open(filepath, 'wb') as f:
            pickle.dump({'mappings': self.mappings, 'inverse_mappings': self.inverse_mappings}, f)
    
    @classmethod
    def load(cls, filepath):
        encoder = cls()
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
            encoder.mappings = data['mappings']
            encoder.inverse_mappings = data['inverse_mappings']
        return encoder
    



import pandas as pd
import requests
import folium
import time
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
def plot_location_iq_map(api_key, csv_file, city=None, address=None):
    """
    Plot a map using LocationIQ API and mark addresses from a CSV file.
    
    Args:
        api_key (str): Your LocationIQ API key
        csv_file (str): Path to CSV file containing addresses
        city (str, optional): City name to filter addresses
        address (str, optional): Specific address to plot
        
    Returns:
        folium.Map: A map with marked locations
    """
    def geocode_address(api_key, address):
        """Helper function to geocode a single address with error handling"""
        try:
            url = f"https://us1.locationiq.com/v1/search.php?key={api_key}&q={address}&format=json"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            if isinstance(data, list) and len(data) > 0:
                return float(data[0]['lat']), float(data[0]['lon'])
            elif isinstance(data, dict) and 'error' in data:
                print(f"Geocoding error for '{address}': {data['error']}")
            else:
                print(f"Unexpected response format for '{address}'")
            return None
        except Exception as e:
            print(f"Failed to geocode address: {address}. Error: {str(e)}")
            return None

    try:
        # Read the CSV file
        df = pd.read_csv(csv_file)
        
        if address:
            # Geocode the single address
            coords = geocode_address(api_key, address)
            if not coords:
                return None
                
            lat, lon = coords
            m = folium.Map(location=[lat, lon], zoom_start=14)
            
            # Add marker for the address
            folium.Marker(
                [lat, lon],
                popup=f"<b>Address:</b> {address}",
                icon=folium.Icon(color='red')
            ).add_to(m)
            
        elif city:
            # Filter addresses by city
            city_addresses = df[df['City'].str.lower() == city.lower()]
            
            if len(city_addresses) > 0:
                # Find first valid address to center the map
                base_lat, base_lon = None, None
                for idx, row in city_addresses.iterrows():
                    coords = geocode_address(api_key, row['Address'])
                    if coords:
                        base_lat, base_lon = coords
                        break
                
                if not base_lat:
                    print(f"Could not geocode any addresses in {city}")
                    return None
                
                m = folium.Map(location=[base_lat, base_lon], zoom_start=12)
                
                # Geocode and mark all addresses
                for idx, row in city_addresses.iterrows():
                    coords = geocode_address(api_key, row['Address'])
                    if coords:
                        lat, lon = coords
                        folium.Marker(
                            [lat, lon],
                            popup=f"<b>Address:</b> {row['Address']}",
                            icon=folium.Icon(color='blue')
                        ).add_to(m)
                    # Add delay to avoid rate limiting
                    time.sleep(2)
                
            else:
                print(f"No addresses found in {city}")
                return None
                
        else:
            print("Please provide either a city or an address")
            return None
            
        return m
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

# Example usage:
# api_key = "your_locationiq_api_key"
# map1 = plot_location_iq_map(api_key, "restaurants.csv", address="1600 Amphitheatre Parkway, Mountain View, CA")
# map2 = plot_location_iq_map(api_key, "restaurants.csv", city="Coimbatore")
# if map1: map1.save("single_address.html")
# if map2: map2.save("city_restaurants.html")


def find_geocode_adress(address, api_key):
    """Helper function to geocode a single address with error handling"""
    try:
        url = f"https://us1.locationiq.com/v1/search.php?key={api_key}&q={address}&format=json"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if isinstance(data, list) and len(data) > 0:
            return float(data[0]['lat']), float(data[0]['lon'])
        elif isinstance(data, dict) and 'error' in data:
            print(f"Geocoding error for '{address}': {data['error']}")
        else:
            print(f"Unexpected response format for '{address}'")
        return None
    except Exception as e:
        print(f"Failed to geocode address: {address}. Error: {str(e)}")
        return None
        
    
    # Geocode the single address
    
    
    #coords = geocode_address(api_key, address)
    #if  not coords:
    #       return None
                
    #lat, lon = coords
    
    
'''m = folium.Map(location=[lat, lon], zoom_start=14)
            
            # Add marker for the address
folium.Marker(
                [lat, lon],
                popup=f"<b>Address:</b> {address}",
                icon=folium.Icon(color='red')
            ).add_to(m)'''