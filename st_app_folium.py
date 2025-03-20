import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster

# Sample DataFrame with Paris addresses, latitude, longitude, and inhabitants
data = {
    "address": ["Eiffel Tower", "Louvre Museum", "Notre-Dame Cathedral"],
    "latitude": [48.8584, 48.8606, 48.8529],
    "longitude": [2.2945, 2.3376, 2.3500],
    "inhabitants": [100, 150, 200]
}
df = pd.DataFrame(data)

# Streamlit App
st.title("Paris Address Map with Inhabitants")

# Create a folium map centered in Paris
m = folium.Map(location=[48.8566, 2.3522], zoom_start=12)
marker_cluster = MarkerCluster().add_to(m)

# Add markers to the map
for _, row in df.iterrows():
    folium.Marker(
        location=[row["latitude"], row["longitude"]],
        popup=f"{row['address']}<br>Inhabitants: {row['inhabitants']}",
        tooltip=f"Inhabitants: {row['inhabitants']}"
    ).add_to(marker_cluster)

# Display the map in Streamlit
st_folium(m)