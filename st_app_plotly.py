import pandas as pd
import numpy as np
import warnings
import os
import random
import pydeck
from pydeck.types import String
import geopandas as gpd
import requests
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import plotly.express as px

color_nuance = {
    'UG': [255, 0, 84], 
    'REC': [0, 29, 61], 
    'EXG': [208, 0, 0], 
    'ENS': [114, 9, 183], 
    'LR': [58, 12, 163], 
    'RN': [0, 53, 102], 
    'DIV': [173, 181, 189], 
    'DVD': [63, 55, 201], 
    'REG': [234, 200, 188], 
    'DVC': [108, 117, 125],
    'ECO': [118, 200, 147], 
    'DVG': [232, 93, 4], 
    'UXD': [0, 0, 0], 
    'EXD': [17, 0, 28],
    'DSV': [53, 1, 44]
}
dict_plotly = {'Ensemble ! (Majorité présidentielle)': 'rgb(114, 9, 183)',
 'Union de la Gauche': 'rgb(255, 0, 84)',
 'Divers droite': 'rgb(63, 55, 201)',
 'Divers gauche': 'rgb(232, 93, 4)',
 'Divers centre': 'rgb(108, 117, 125)'}
custom_data_df = geodata_final_copy[["election","adresse_bv","inscrits","perc_abstentions","nom_prenom","perc_voix_exprimes","Libellé"]]

fig = px.scatter_mapbox(
    geodata_final_copy,
    lat="latitude",
    lon="longitude",
    color="Libellé",  # Plotly recognizes RGB strings
    animation_frame="election",  # Animate by election year
    # hover_name="neighbour",
    title="Paris Local Election Results",
    mapbox_style="open-street-map",
    zoom=10,  # Adjust zoom level
    center={"lat": 48.8566, "lon": 2.3522},  # Center on Paris,
    size="size",
    size_max=10,
    color_discrete_map=dict_plotly,
    # hover_data={"hover_text": True, "Libellé": False, "longitude": False, "latitude": False, "size":False, "election": False},
    # hovertemplate={"<b>Election:</b> {row['election']}<br>"
    #             "<b>Bureau de vote:</b> {row['adresse_bv']}<br>"
    #             "<b>Nb inscrits:</b> {row['inscrits']}<br>"}
)
# Enable scroll zoom
fig.update_layout(
    mapbox=dict(
        # accesstoken="",  # Optional: Add your Mapbox token if using a custom style
        zoom=12,  # Initial zoom level
    ),
    margin={"r": 0, "t": 50, "l": 0, "b": 0},
    dragmode="pan",  # Allows dragging the map
)
# Set custom width & height for the map
fig.update_layout(
    mapbox_bounds={"west": 2.25, "east": 2.45, "south": 48.81, "north": 48.91},
    width=1200,  # Adjust map width
    height=800,  # Adjust map height
)

fig.update_traces(
    marker=dict(sizemode="area"),
    customdata=custom_data_df,
    hovertemplate="<b>Election:</b> {custom_data_df[0]}<br>"
                "<b>Bureau de vote:</b> {custom_data_df[1]}<br>"
                "<b>Nb inscrits:</b> {custom_data_df[2]}<br>")  # Custom data for score
                
# Enable zooming with the mouse scroll wheel
fig.show(config={"scrollZoom": True})