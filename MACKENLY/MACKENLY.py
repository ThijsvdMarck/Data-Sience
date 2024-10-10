#%% Importeer de benodigde bibliotheken
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
import pandas as pd
import os
# need to be added
from streamlit_folium import st_folium 
from folium.plugins import MarkerCluster
import folium
from folium.plugins import HeatMap

# %% Streamlit1

# Define the function for displaying the map of charging stations (laadpalen)
def laadpalen_kaart_adres_staat(df):
    # Streamlit app title and explanation in Dutch
    st.title("Laadpalen in Nederland")
    st.header("Interactieve kaart van laadpalen")
    st.write("""
    Deze interactieve kaart toont de locaties van laadpalen voor elektrische voertuigen in Nederland.
    Gebruik de zijbalk om laadpalen te filteren op plaats. Klik op de markeringen voor meer details over elke laadpaal,
    het adres, plaats en postcode.
    """)

    # Create a Streamlit sidebar with a multi-select widget for towns
    selected_towns = st.sidebar.multiselect('Selecteer Plaatsen', df['AddressInfo.Town'].unique())

    # Filter the dataframe based on selected towns
    if selected_towns:
        df = df[df['AddressInfo.Town'].isin(selected_towns)]

    # Create a base map centered at the average latitude and longitude of the data
    latitude_mean = df['AddressInfo.Latitude'].mean()
    longitude_mean = df['AddressInfo.Longitude'].mean()
    map_laadpalen = folium.Map(location=[latitude_mean, longitude_mean], zoom_start=6.5)

    # Add marker clusters to the map
    marker_cluster = MarkerCluster().add_to(map_laadpalen)

    # Iterate through the DataFrame and add points
    for idx, row in df.iterrows():
        latitude = row['AddressInfo.Latitude']
        longitude = row['AddressInfo.Longitude']
        town = row['AddressInfo.Town']
        address_info = row['AddressInfo.Title']
        postcode = row['AddressInfo.Postcode']  # Extracting postcode

        # Create the popup content with postcode added
        popup_content = f"<b>Adres:</b> {address_info}<br><b>Plaats:</b> {town}<br><b>Postcode:</b> {postcode}"
        popup = folium.Popup(popup_content, max_width=300)  # Adjust the max_width as needed

        # Add marker with popup
        folium.Marker(
            location=[latitude, longitude],
            popup=popup,
            icon=folium.Icon(color='blue')  # Use a default color for the marker
        ).add_to(marker_cluster)

    # Display the map in the Streamlit app using st_folium
    st_folium(map_laadpalen, width=700, height=500)

# laadpalen_kaart_adres_staat(LaadpalenPunten)
 



#%%  used a Nominatim API to fill AddressInfo.StateOrProvince to use as revelant data
# import time
# import pandas as pd
# from geopy.geocoders import Nominatim

# # Load your CSV file
# LaadpalenPunten

# # Initialize Nominatim API for geocoding
# geolocator = Nominatim(user_agent="geoapiExercises")

# # List of the 12 provinces in the Netherlands
# valid_provinces = [
#     'Drenthe', 'Flevoland', 'Friesland', 'Gelderland', 'Groningen', 'Limburg',
#     'North Brabant', 'North Holland', 'Overijssel', 'South Holland', 'Utrecht', 'Zeeland'
# ]

# # Function to get state/province from latitude and longitude, with one retry if the first attempt fails
# def get_state(lat, lon):
#     try:
#         # First attempt
#         location = geolocator.reverse((lat, lon), language='en')
#         address = location.raw['address']
#         state = address.get('state', '')

#         # Only return state if it's a valid Dutch province
#         if state in valid_provinces:
#             return state
#         else:
#             return None
#     except Exception as e:
#         # If the first attempt fails, try again once
#         try:
#             time.sleep(1)  # Brief delay before retrying
#             location = geolocator.reverse((lat, lon), language='en')
#             address = location.raw['address']
#             state = address.get('state', '')

#             # Only return state if it's a valid Dutch province
#             if state in valid_provinces:
#                 return state
#             else:
#                 return None
#         except:
#             # If the second attempt also fails, return None
#             return None

# # Fill missing 'StateOrProvince' values
# for index, row in LaadpalenPunten.iterrows():
#     if pd.isnull(row['AddressInfo.StateOrProvince']):
#         state = get_state(row['AddressInfo.Latitude'], row['AddressInfo.Longitude'])
#         LaadpalenPunten.at[index, 'AddressInfo.StateOrProvince'] = state
#         time.sleep(1)  # Add a delay of 1 second to avoid rate limiting

# # Save the updated dataframe to a new CSV file
# LaadpalenPunten.to_csv('laadpalenpunt_met_state.csv', index=False)


# # checking for missing valeus
# missing_valuesA = LaadpalenPunten.isna().sum()
# print(missing_valuesA)
# #Updated from 7432 open valeu file have 771 province open valeu aprox 10% of total data,
# # but still think its enouch data to use had to save it as csv file cuz it took a total of 210min to run

#%% Streamlit2

# Define a function that takes a DataFrame as input
def laadpalen_visualization(df):
    # Filter out missing values in 'AddressInfo.StateOrProvince'
    df_provinces = df.dropna(subset=['AddressInfo.StateOrProvince'])

    # Task 1: Circle Diagram (Pie Chart)
    st.title("Percentage of Charging Stations by Province")

    # Count occurrences of each province
    province_counts = df_provinces['AddressInfo.StateOrProvince'].value_counts()

    # Create a pie chart using Plotly
    fig_pie = px.pie(province_counts, values=province_counts.values, names=province_counts.index, 
                     title="Percentage of Charging Stations by Province", hole=0.4)
    st.plotly_chart(fig_pie)

    # Task 2: Heatmap of Charging Stations by Province
    st.title("Heatmap of Charging Stations by Province")

    # Group the data by province and get the counts
    province_lat_lon = df_provinces[['AddressInfo.StateOrProvince', 'AddressInfo.Latitude', 'AddressInfo.Longitude']]
    province_grouped = province_lat_lon.groupby('AddressInfo.StateOrProvince').count()

    # Create a base map centered on the Netherlands
    m = folium.Map(location=[52.1326, 5.2913], zoom_start=7)

    # Prepare data for HeatMap
    heat_data = [[row['AddressInfo.Latitude'], row['AddressInfo.Longitude']] for index, row in df_provinces.iterrows()]

    # Add the heatmap layer
    HeatMap(heat_data).add_to(m)

    # Display the map in Streamlit
    st_folium(m, width=700, height=500)

# Example of calling the function with a DataFrame
# Load CSV data into a dataframe
laadpalenpunt_met_state = pd.read_csv('laadpalenpunt_met_state.csv')

# laadpalen_visualization(laadpalenpunt_met_state)

