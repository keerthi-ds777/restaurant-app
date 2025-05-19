import streamlit as st
import pandas as pd
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os
from functions import find_geocode_adress
import joblib
import webbrowser
import numpy as np
import folium
from streamlit_folium import st_folium


# Set page configuration

st.set_page_config(
    page_title="BiteFinder",
    page_icon="🍔",
    layout="wide"
)

load_dotenv()


dfd = pd.read_csv(r'C:\Users\loges\Desktop\python\sample projects\GUVI\restaurant\data\clustered_data.csv')
df = pd.read_csv(r'C:\Users\loges\Desktop\python\sample projects\GUVI\restaurant\data\restaurant_encoded_features.csv')
dfc = pd.read_csv(r'C:\Users\loges\Desktop\python\sample projects\GUVI\restaurant\data\restaurant_features (3).csv')

dfc['Clusters'] = dfd['cluster']

cusine_dic = {}
city_dic = {}
rating_dic = {}
price_range_dic	= {}
online_delivery_dic={}
tabel_booking_dic={}
avg_cost_two_dic ={}

cusine_list = list(dfc['Cuisines'].unique())
city_list = list(dfc['City'].unique())
rating_list = list(dfc['Rating_text'].unique())
online_delivery_list = list(dfc['Online Delivery'].unique())
tabel_booking_list = list(dfc['Table Booking'].unique())

for i, j in zip(dfc['Average Cost for Two'], df['Average Cost for Two']):
   city = {f"{i}": j}
   avg_cost_two_dic.update(city)


for i, j in zip(dfc['Table Booking'], df['Table Booking']):
   city = {f"{i}": j}
   tabel_booking_dic.update(city)


for i, j in zip(dfc['Online Delivery'], df['Online Delivery']):
   city = {f"{i}": j}
   online_delivery_dic.update(city)



for i, j in zip(dfc.Rating_text, df.Rating_text):
   city = {f"{i}": j}
   rating_dic.update(city)


for i, j in zip(dfc['Price Range'], df['Price Range']):
   city = {f"{i}": j}
   price_range_dic.update(city)


for i, j in zip(dfc.City, df.City):
   city = {f"{i}": j}
   city_dic.update(city)


for i, j in zip(dfc.Cuisines, df.Cuisines):
   cusine = {f"{i}": j}
   cusine_dic.update(cusine)



# Initialize session state for page navigation
if "page" not in st.session_state:
    st.session_state.page = "home"
if "map_data" not in st.session_state:
    st.session_state.map_data = None



# Custom CSS for styling
st.markdown(
    """
    <style>
        .main {background-color: #121212; color: white;}
        .sidebar .sidebar-content {background-color: #1E1E1E;}
        .stSlider {color: red;}
        .stRadio label {color: white;}
    </style>
    """,
    unsafe_allow_html=True,
)

# loading the model
@st.cache_resource
def model_loader(path):
    model=joblib.load(path)
    return model

#loading both models 
with st.spinner("Hold on, the app is loading..."):
    model = model_loader(r"data/cluster_model.pkl")

# Sidebar Filters
st.sidebar.image("https://b.zmtcdn.com/data/pictures/chains/2/308322/348dfe37e84fba7f22131948a62d8519.jpg?output-format=webp&fit=around|771.75:416.25&crop=771.75:416.25;*,*",
                  use_container_width=True)
st.sidebar.header("🔎 Filter Your Search")
st.sidebar.subheader("🍽️ Find Your Perfect Restaurant")



cusine = st.sidebar.selectbox("🍽️ Enter Cuisine Type",options=cusine_list,help="You can get your prefered cuisines")
cusine_v =cusine 
cusine = cusine_dic[cusine]

location = st.sidebar.selectbox(
    "📍 Enter Your Location",
    options=city_list,
    help="You can get a collection of locations in the particular city"
)
location_v= location
location = city_dic[location]

rating = st.sidebar.selectbox("⭐ Kind of rating would you prefer", options=rating_list)
rating_v = rating
rating = rating_dic[rating]

price_range = st.sidebar.slider(
    "💰 Price Range", 
    max_value=4, 
    value=(1, 4),  # Default range
    step=1, 
    help="Select the price range of the restaurant")

online_delivery = st.sidebar.selectbox("select if the restaurent has Online Delivery", options=online_delivery_list, help="Select if you want online delivery")
online_delivery_v = online_delivery
online_delivery = online_delivery_dic[online_delivery]

tabel_booking = st.sidebar.selectbox("select if the restaurent has Table Booking", options=tabel_booking_list, help="Select if you want table booking")
tabel_v = tabel_booking
tabel_booking = tabel_booking_dic[tabel_booking]

avg_cost_two = st.sidebar.number_input("select the average cost for two", help="Select the average cost for two")
avg_cost_two = float(avg_cost_two)

# Handle price_range (convert tuple to a single value, e.g., average)
price_range_value = sum(price_range) / len(price_range)  # Calculate the average of the range

# Create the input array with consistent numeric values
input_arry = np.array([
    cusine, location, rating, price_range_value, online_delivery, tabel_booking, avg_cost_two
], dtype=float)  # Ensure all elements are numeric
input_arry = input_arry.reshape(1, -1)
# Assuming the model was trained with these feature names
feature_names = ['Cuisines', 'City', 'Rating_text', 'Price Range', 
                 'Online Delivery', 'Table Booking', 'Average Cost for Two']

# Convert input_arry to a DataFrame with feature names
input_df = pd.DataFrame(input_arry, columns=feature_names)

# Predict the cluster
cluster = model.predict(input_df)

# Predict button
predict = st.sidebar.button('Predict')

if predict:
    # Predicting the cluster
    cluster = model.predict(input_arry)

    # Filter the cluster data
    cluster_df = dfc[dfc['Clusters'] == cluster[0]]  # Ensure 'Clusters' column is used correctly

    # Apply additional filters
    new_df = cluster_df[
        (cluster_df['Cuisines'] == cusine_v) &
        (cluster_df['City'] == location_v) &
        (cluster_df['Rating_text'] == rating_v) &
        (cluster_df['Price Range'] == price_range_value) &
        (cluster_df['Online Delivery'] == online_delivery_v) &
        (cluster_df['Table Booking'] == tabel_v) &
        (cluster_df['Average Cost for Two'] == avg_cost_two)
    ]

    # Check if the filtered DataFrame is empty
    if new_df.empty:
        st.warning("No results found for the selected filters. Showing all restaurants in the cluster.")
        new_df = cluster_df  # Show all data in the cluster

    # Display the filtered or fallback DataFrame
    st.markdown("<h1 style='text-align: center; color: #FF5733;'>BiteFinder: Real-Time & Static Restaurant Recommendations</h1>", unsafe_allow_html=True)

    st.markdown("#### Explore the best dining options tailored to your preferences!")

    st.write("BiteFinder | A Personalized Dining Guide | Location Guidence")
    
    st.markdown("### 🎉 Recommended Restaurants")
    for idx, row in new_df.iterrows():
        with st.container():
            # Display restaurant name
            st.markdown(f"#### {row['Name']}")

            # Display photo
            if 'Photo_urls' in row and pd.notna(row['Photo_urls']):
                st.image(row['Photo_urls'], width=300)

            # Display location
            st.markdown(f"**Location:** {row['Address']}")

            # Display cuisine
            st.markdown(f"**Cuisine:** {row['Cuisines']}")

            # Display rating
            st.markdown(f"**Rating:** {row['Rating_text']}")

            # Display price range
            st.markdown(f"**Price Range:** {row['Price Range']}")

            # Display online delivery and table booking
            st.markdown(f"**Online Delivery:** {row['Online Delivery']}")
            st.markdown(f"**Table Booking:** {row['Table Booking']}")

            # Display average cost for two
            st.markdown(f"**Average Cost for Two:** {row['Average Cost for Two']}")

            # Display URL
            if 'URL' in row and pd.notna(row['URL']):
                st.markdown(f"[Visit Website]({row['URL']})", unsafe_allow_html=True)
            # Add a "Find Location" button
            # Add a "Find Location" button
            # Find Location Button
            if st.button(f"📍 Find Location", key=f"btn_{idx}"):
              
          
       
                # Embed Google Maps iframe
                map_html = f"""
                    <iframe 
                        width="700" 
                        height="500" 
                        frameborder="0" 
                        style="border:0" 
                        src="https://www.google.com/maps?q={row['Latitude']},{row['Longitude']}&hl=es;z=14&output=embed" 
                        allowfullscreen>
                    </iframe>
                """
                st.components.v1.html(map_html, height=500)
           
    



    st.markdown("### Recommended Restaurants")
    
# Display the filtered DataFrame

    # Main Section
st.markdown("<h1 style='text-align: center; color: #FF5733;'>BiteFinder: Real-Time & Static Restaurant Recommendations</h1>", unsafe_allow_html=True)

st.markdown("#### Explore the best dining options tailored to your preferences!")

st.write("BiteFinder | A Personalized Dining Guide | Location Guidence")



