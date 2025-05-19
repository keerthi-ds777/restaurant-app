import streamlit as st
import folium
from streamlit_folium import st_folium
from dotenv import load_dotenv
import os
from App.functions import find_geocode_adress

# Load environment variables
load_dotenv()

def map_page():
    st.title("📍 Map Page")
    
    # Retrieve location details from session state
    map_data = st.session_state.get("map_data", None)
    if map_data:
        address = map_data["address"]
        name = map_data["name"]
        
        # Fetch coordinates using LocationIQ API
        api_key = os.getenv("LOCATIONIQ_API_KEY")
        coords = find_geocode_adress(address, api_key)
        
        if coords:
            lat, lon = coords
            st.markdown(f"### Location for {name}")
            st.markdown(f"**Address:** {address}")
            
            # Create a folium map centered on the location
            m = folium.Map(location=[lat, lon], zoom_start=15)
            folium.Marker([lat, lon], popup=name).add_to(m)
            
            # Display the map in Streamlit
            st_folium(m, width=700, height=500)
        else:
            st.error("Could not fetch coordinates for the given address.")
        
        # Back button
        if st.button("Back to Home"):
            st.session_state.page = "home"
            st.experimental_rerun()
    else:
        st.error("No location data available. Please go back and try again.")