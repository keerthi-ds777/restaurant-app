import streamlit as st
import folium
from streamlit_folium import st_folium

def map_page(latitude, longitude, name="Selected Location"):
    st.title("📍 Map Page")

    if latitude is not None and longitude is not None:
        st.markdown(f"### Location for {name}")
        st.markdown(f"**Coordinates:** Latitude: {latitude}, Longitude: {longitude}")

        # Create a folium map centered on the location
        m = folium.Map(location=[latitude, longitude], zoom_start=15)
        folium.Marker([latitude, longitude], popup=name).add_to(m)

        # Display the map in Streamlit
        st_folium(m, width=700, height=500)
    else:
        st.error("Could not fetch valid coordinates for the given location.")

    # Back button
    if st.button("Back to Home"):
        st.session_state.page = "home"
        st.experimental_rerun()