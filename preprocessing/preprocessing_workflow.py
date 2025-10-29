import json
import pandas as pd

from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
#load_dotenv()
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder




class Workflow:

    def __init__(self):

        self.df= None
        self.features = None
        self.scaled = None
    
    def data_load(self,n:int=1,m: int=6):
        
        restaurants = []
        # Loop through the range of number of files 
        # Be aware of the names of the files should be number ranging from n and m
        for i in range(n,m):
            # Load JSON file
            with open(r'/Users/lravi/Documents/Github/restaurant-app/data/file{}.json'.format(i), "r", encoding="utf-8") as file:
                data = json.load(file)

            # Extract relevant information
            for item in data:  # data is a list, so iterate directly
                if isinstance(item, dict) and "restaurants" in item:  # Ensure correct structure
                    for rest in item["restaurants"]:
                        restaurant = rest["restaurant"]
                        restaurants.append({
                            "ID": restaurant.get("id"),
                            "Name": restaurant.get("name"),
                            "Cuisines": restaurant.get("cuisines"),
                            "Address": restaurant["location"].get("address"),
                            "City": restaurant["location"].get("city"),
                            "Rating": restaurant["user_rating"].get("aggregate_rating"),
                            "Rating_text": restaurant["user_rating"].get("rating_text"),
                            "Votes": restaurant["user_rating"].get("votes"),
                            "Price Range": restaurant.get("price_range"),
                            "Latitude": restaurant["location"].get("latitude"),
                            "Longitude": restaurant["location"].get("longitude"),
                            "Online Delivery": "Yes" if restaurant.get("has_online_delivery") else "No",
                            "Table Booking": "Yes" if restaurant.get("has_table_booking") else "No",
                            "Average Cost for Two": restaurant.get("average_cost_for_two"),
                            "Photo_urls": restaurant.get("photos_url"),
                            'Url': restaurant.get('url')
                        })
        # Convert to DataFrame
        self.df = pd.DataFrame(restaurants)
        features = ['City','Rating', 'Votes',
                    'Price Range','Online Delivery',
                    'Table Booking', 'Average Cost for Two']  # adjust as needed
        
        self.features = self.df[features]

        print('Data is succusfully retrived json and returned as pd.DataFrame')
        #return df
    

    def preprocess(self):
        if self.features is not None:
            cat_col= self.features.select_dtypes(include=["object", "category"]).columns
            
            col_name=self.features.columns
            le = LabelEncoder()
            
            for i in cat_col:
                self.features[i] = le.fit_transform(self.features[i].astype(str))

            
            scaler = StandardScaler()
            scaled = scaler.fit_transform(self.features)
            
            scaled_df = pd.DataFrame(scaled, columns=col_name)
            self.scaled = scaled_df if not scaled_df.empty else None
            


            print('Processed Data is succusfully assigned to self.scaled attribute')
        else:
            print("DataFrame is empty. Please load data first.")
    
    def fit_model(self,n_clusters:int, random_state=42, return_score=False, model_save=False):
    
    
        kmeans = KMeans(n_clusters=n_clusters, random_state=random_state)

    
        if self.scaled is None:
            raise ValueError("Scaled data is not available. Please ensure 'preprocess' is called successfully before fitting the model.")
        labels = kmeans.fit_predict(self.scaled)
        score = silhouette_score(self.scaled, labels)
        
        print(f'KMeans model with {n_clusters} clusters fitted and saved to sql database')
        if return_score==True:
            return kmeans, score
        else:
         return kmeans
        if model_save==True:
            import joblib
            joblib.dump(kmeans, r'/Users/lravi/Documents/Github/restaurant-app/data/kmeans_model.pkl')    


    def save_to_sql(self):#,Engine=engine):
        if self.df is not None:
            self.df.to_csv('/Users/lravi/Documents/Github/restaurant-app/data/restaurent_table.csv', index=False)
        if self.features is not None:
            self.features.to_csv('/Users/lravi/Documents/Github/restaurant-app/data/features_for_clustering.csv', index=False)
        if self.scaled is not None:
            self.scaled.to_csv('/Users/lravi/Documents/Github/restaurant-app/data/clustered_data.csv', index=False)
        print('DataFrames are successfully saved to sql database')
    
    def main(self,n_cluster:int=20,return_score=False,model_save=False,sql_save=False):
        self.data_load()  # Replace 1 and 10 with appropriate values
        self.preprocess()
        result = self.fit_model(n_clusters=n_cluster, return_score=return_score,model_save=model_save)
        if return_score:
            if isinstance(result, tuple):
                model, score = result
                print(f'Silhouette Score: {score}')
                if sql_save:
                    self.save_to_sql()
                return model, score
        else:
            if sql_save:
                self.save_to_sql()
            return result
        

if __name__ == "__main__":
    workflow = Workflow()
    model=workflow.main(n_cluster=20,return_score=True,model_save=True,sql_save=True)
    print("Preprocessing workflow completed.")
            #or
    """workflow=Workflow()
    workflow.data_load(n=1,m=6)
    workflow.preprocess()
    model=workflow.fit_model(n_clusters=4, return_score=False,model_save=False)
    workflow.save_to_sql(Engine=engine)
    print("Preprocessing workflow completed.")"""