# # -*- coding: utf-8 -*-
# Case 2 Team 20 - Thijs van der Marck, Rob van der Vaart, Jelle van der Wal

#%% Importeer de benodigde bibliotheken
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
import pandas as pd
import os 
import requests


import THIJS.TVDM as tv
# import ARGENIS.ARGENIS as ar
import MACKENLY.MACKENLY as ma
import TIM.TIM as tl





#%% Load Kaggle API data
# os.environ['KAGGLE_USERNAME'] = 'thijsvandermarck'
# os.environ['KAGGLE_KEY'] = '07f3e809702e7b2b43e9e7d4858933f1'
 
# kg.api.authenticate()
 
# kg.api.dataset_download_files(dataset = "moazzimalibhatti/co2-emission-by-countries-year-wise-17502022", path='on.zip', unzip=True)

response = requests.get("https://api.openchargemap.io/v3/poi/?output=json&countrycode=NL&maxresults=10000&compact=true&verbose=false&key=93b912b5-9d70-4b1f-960b-fb80a4c9c017")
responsejson  = response.json()
Laadpalen = pd.json_normalize(responsejson)
# print(Laadpalen)


columns_to_drop = [
    #For useless or not  informative columns
    'ID',
    'UUID',
    'Connections',
    'Reference'
]

missing_values = Laadpalen.isna().sum()
print(missing_values)

LaadpalenPunten = Laadpalen.drop(columns=columns_to_drop, errors='ignore')




# # Get the directory where the current script is located
current_dir = os.path.dirname(os.path.abspath(__file__))
print(current_dir)



# # Build the path to the CSV file in the subfolder
file_path = os.path.join(current_dir, 'DATA', 'laadpaaldata.csv')
print(file_path)


# # Reading the CSV file
LaadpalenGebruik = pd.read_csv(file_path)
print(LaadpalenGebruik.head())
print(LaadpalenGebruik.info())

# Build the path to the CSV file in the subfolder
file_path = os.path.join(current_dir, 'DATA', 'cars.csv')

# Reading the CSV file
ElektrischeAutos = pd.read_csv(file_path) #moet nog met API en schoongemaakt worden



#%%__________________________________________________________________________________
#%% Streamlit
tv.LayoutSettings()


page = tv.DropdownForPageSelect()
if page == "Laadpaal Punten":
    # "Laadpaal Punten"
    print("Laadpaal Punten")
elif page == "Laadpaal Gebruik":
    # LaadpalenGebruik
    # tl.gebruik(LaadpalenGebruik)
    print("Laadpaal Gebruik")
elif page == "Elektrische  Auto's":
    # ElektrischeAutos
    tv.plotAantalElektrischeAutosTegenDatum(ElektrischeAutos)



















# #%% Eerst plot
# # Streamlit UI opzetten
# st.title('CO2 Emissions per Country')

# # Landen in dropdown selecteren 
# countries = df['Country'].unique()
# selected_country = st.selectbox('Select a country', countries)
# country_data = df[df['Country'] == selected_country]

# # Groepeer de data per jaar en maak lineplot met plotly voor CO2 emission
# country_data_groupby = country_data.groupby('Year')['CO2 emission (Tons)'].sum().reset_index()
# country_data_groupby_non_zero = country_data_groupby[country_data_groupby['CO2 emission (Tons)'] > 0]
# fig = px.line(country_data_groupby_non_zero, x='Year', y='CO2 emission (Tons)', title=f'CO2 Emissions in {selected_country} per year')
# fig.update_xaxes(dtick=10)
# fig.update_yaxes(range=[0, country_data_groupby['CO2 emission (Tons)'].max()])
# st.plotly_chart(fig)

# # Filtered country data (only showing the first row)
# country_table = country_data[['Country', 'Area', '% of World', 'Population(2022)']]

# # KPIs for the selected country
# st.write(f"#### Key Metrics for {selected_country}")

# # Extracting the first row values for KPI
# area = country_table.iloc[0]['Area']
# percentage_of_world = country_table.iloc[0]['% of World']
# population = country_table.iloc[0]['Population(2022)']

# # Display KPIs in a clean 3-column layout
# col1, col2, col3 = st.columns(3)

# with col1:
#     st.metric(
#         label="Area",
#         value=f"{area:,.0f} km²",  # Formatting with commas for thousands
#         delta=None
#     )

# with col2:
#     st.metric(
#         label="% of World",
#         value=f"{percentage_of_world:.2f}%",  # Formatting with 2 decimal places for percentage
#         delta=None
#     )

# with col3:
#     st.metric(
#         label="Population (2022)",
#         value=f"{population:,.0f}",  # Formatting with commas for large numbers
#         delta=None
#     )

# # Add a separator line for better readability
# st.markdown("---")

# # Add some context text for the KPIs
# st.write("""
# ##### Notes:
# - **Area** refers to the total land area in square kilometers.
# - **% of World** shows the percentage of total global land area occupied by this country.
# - **Population (2022)** shows the estimated population of the country in 2022.
# """)
# #%% Tweede plot met twee landen vergelijking
# # Streamlit UI opzetten
# st.title('Comparing CO2 statistics of two countries')

# # Maak een dropdown om tussen CO2 en CO2 per capita te wisselen
# plot_type = st.selectbox('Select plot type', ['CO2 Emissions per Capita','Comparing CO2 Emissions per km²']) #, 'Comparing CO2 Emissions% per km²

# # Landen in dropdown selecteren 
# countries = merged_df['Country'].unique()

# # Selecteer twee landen
# selected_country1 = st.selectbox('Select country 1', countries)
# selected_country2 = st.selectbox('Select country 2', countries)

# # Data voor de twee landen
# country_data1 = merged_df[merged_df['Country'] == selected_country1]
# country_data2 = merged_df[merged_df['Country'] == selected_country2]

# # Voor de eerste plot
# country_data1_groupby = country_data1.groupby('Year')[['Population', 'CO2 emission (Tons)']].sum().reset_index()
# country_data1_groupby['Population_per_CO2'] = country_data1_groupby['CO2 emission (Tons)'] / country_data1_groupby['Population']

# country_data2_groupby = country_data2.groupby('Year')[['Population', 'CO2 emission (Tons)']].sum().reset_index()
# country_data2_groupby['Population_per_CO2'] = country_data2_groupby['CO2 emission (Tons)'] / country_data2_groupby['Population']

# country_data1_groupby_non_zero = country_data1_groupby[country_data1_groupby['CO2 emission (Tons)'] > 0]
# country_data2_groupby_non_zero = country_data2_groupby[country_data2_groupby['CO2 emission (Tons)'] > 0]

# # Voor de tweede plot

# country_data3_groupby = country_data1.groupby('Year')[['Area', 'CO2 emission (Tons)']].sum().reset_index()
# country_data3_groupby['Area_per_CO2'] = (country_data3_groupby['CO2 emission (Tons)'] / country_data3_groupby['Area'])

# country_data4_groupby = country_data2.groupby('Year')[['Area', 'CO2 emission (Tons)']].sum().reset_index()
# country_data4_groupby['Area_per_CO2'] = (country_data4_groupby['CO2 emission (Tons)'] / country_data4_groupby['Area'])

# country_data3_groupby_non_zero = country_data3_groupby[country_data3_groupby['CO2 emission (Tons)'] > 0]
# country_data4_groupby_non_zero = country_data4_groupby[country_data3_groupby['CO2 emission (Tons)'] > 0]

# # #Derde plot ZIT EEN REKENFOUT IN
# # merged_df['CO2 emission (%)'] = 0.0

# # # Iterate over each unique year
# # for year in merged_df['Year'].unique():
# #     # Filter data for the specific year
# #     year_data = merged_df[merged_df['Year'] == year]
        
# #     # Calculate the total CO2 emissions for the year
# #     total_emission = year_data['CO2 emission (Tons)'].sum()
        
# #     # Calculate the percentage for each country and update the 'CO2 emission (%)' column
# #     merged_df.loc[merged_df['Year'] == year, 'CO2 emission (%)'] = (merged_df.loc[merged_df['Year'] == year, 'CO2 emission (Tons)'] / total_emission) * 100


# # # Data voor de twee landen
# # country_data_d = merged_df[merged_df['Country'] == selected_country1]
# # country_data_e = merged_df[merged_df['Country'] == selected_country1]

# # # Groepeer de data per jaar en maak lineplot met plotly voor CO2 emission %
# # country_data_d_groupby = country_data_d.groupby('Year')[['Area', 'CO2 emission (%)']].sum().reset_index()
# # country_data_d_groupby['Area_per_CO2%'] = (country_data_d_groupby['CO2 emission (%)'] / country_data_d_groupby['Area'])

# # country_data_e_groupby = country_data_e.groupby('Year')[['Area', 'CO2 emission (%)']].sum().reset_index()
# # country_data_e_groupby['Area_per_CO2%'] = (country_data_e_groupby['CO2 emission (%)'] / country_data_e_groupby['Area'])

# # country_data_d_groupby_non_zero = country_data_d_groupby[country_data_e_groupby['CO2 emission (%)'] > 0]
# # country_data_e_groupby_non_zero = country_data_e_groupby[country_data_d_groupby['CO2 emission (%)'] > 0]

# # Conditie om te kiezen welk plot te tonen
# if plot_type == 'CO2 Emissions per Capita':

#     fig = px.line(country_data_groupby_non_zero, x='Year', y='CO2 emission (Tons)', title=f'CO2 Emissions in {selected_country} per year')
#     fig.update_yaxes(range=[0, country_data_groupby['CO2 emission (Tons)'].max()])

#     # Maak een enkele lineplot voor de twee landen
#     fig = px.line()
#     fig.add_scatter(x=country_data1_groupby_non_zero['Year'], y=country_data1_groupby_non_zero['Population_per_CO2'], name=selected_country1)
#     fig.add_scatter(x=country_data2_groupby_non_zero['Year'], y=country_data2_groupby_non_zero['Population_per_CO2'], name=selected_country2)
#     fig.update_xaxes(dtick=10)
#     fig.update_yaxes(range=[0, max(country_data1_groupby['Population_per_CO2'].max(), country_data2_groupby['Population_per_CO2'].max())])
#     fig.update_layout(
#         title=f'Amount of CO2 Emissions in {selected_country1} and {selected_country2} per year, per capita',
#         xaxis_title='Year',
#         yaxis_title='Population per CO2 (tons)'
#     )
#     st.plotly_chart(fig)
# elif plot_type == 'Comparing CO2 Emissions per km²':
#     # Maak een enkele lineplot voor de twee landen
#     fig3 = px.line()
#     fig3.add_scatter(
#         x=country_data3_groupby_non_zero['Year'],
#         y=country_data3_groupby_non_zero['Area_per_CO2'],
#         name=selected_country1
#     )
#     fig3.add_scatter(
#         x=country_data4_groupby_non_zero['Year'],
#         y=country_data4_groupby_non_zero['Area_per_CO2'],
#         name=selected_country2
#     )
#     fig3.update_xaxes(dtick=10)
#     fig3.update_yaxes(range=[
#         0,
#         max(
#             country_data3_groupby['Area_per_CO2'].max(),
#             country_data4_groupby['Area_per_CO2'].max()
#         )
#     ])
#     fig3.update_layout(
#         title=f'Amount of CO2 Emissions in {selected_country1} and {selected_country2} per year, per km²',
#         xaxis_title='Year',
#         yaxis_title='CO2 (tons) per km²'
#     )
#     st.plotly_chart(fig3)
# # else: ZIT EEN REKENFOUT IN

# #     # Maak een enkele lineplot voor de twee landen
# #     fig4 = px.line()
# #     fig4.add_scatter(x=country_data_e_groupby_non_zero['Year'], y=country_data_e_groupby_non_zero['Area_per_CO2%'], name=selected_country1)
# #     fig4.add_scatter(x=country_data_d_groupby_non_zero['Year'], y=country_data_d_groupby_non_zero['Area_per_CO2%'], name=selected_country2)
# #     fig4.update_xaxes(dtick=10)
# #     fig4.update_yaxes(range=[0, max(country_data_d_groupby['Area_per_CO2%'].max(), country_data_e_groupby['Area_per_CO2%'].max())])
# #     fig4.update_layout(
# #         title=f'Amount of CO2 Emissions Percentage in {selected_country1} and {selected_country2} per year, per km²',
# #         xaxis_title='Year',
# #         yaxis_title='CO2% per km²'
# #     )
# #     st.plotly_chart(fig4)
# #%% Stats onderaan
# No delta, so no green/red line
#     )
#     st.metric(
#         label=f'{selected_country1} Population',
#         value=f'{population_percentage_country1}%',
#         delta=None  # # Selecteer een jaar.
# selected_year = st.selectbox('Select year', [int(year) for year in merged_df['Year'].unique()])
 
# # Data voor de twee landen in het geselecteerde jaar
# country_data1_year = country_data1[country_data1['Year'] == selected_year]
# country_data2_year = country_data2[country_data2['Year'] == selected_year]
 
# # Bereken de percentages
# global_co2_emission = merged_df[merged_df['Year'] == selected_year]['CO2 emission (Tons)'].sum()
# global_population = merged_df[merged_df['Year'] == selected_year]['Population'].sum()
 
# co2_emission_percentage_country1 = round((country_data1_year['CO2 emission (Tons)'].sum() / global_co2_emission) * 100,3)
# co2_emission_percentage_country2 = round((country_data2_year['CO2 emission (Tons)'].sum() / global_co2_emission) * 100,3)
 
# population_ = st.columns(2)

# with col1:
#     st.metric(
#         label=f'{selected_country1} CO2 Emissions',
#         value=f'{co2_emission_percentage_country1}%',
#         delta=None  # No delta, so no green/red line
#     )

# with col2:
#     st.metric(
#         label=f'{selected_country2} CO2 Emissions',
#         value=f'{co2_emission_percentage_country2}%',
#         delta=None  # No delta, so no green/red line
#     )
#     st.metric(
#         label=f'{selected_country2} Population',
#         value=f'{population_percentage_country2}%',
#         delta=None  # No delta, so no green/red line
#     )percentage_country1 = round((country_data1_year['Population'].sum() / global_population) * 100,3)
# population_percentage_country2 = round((country_data2_year['Population'].sum() / global_population) * 100,3)
 
# # Weergeef de percentages onder de grafiek
# st.write(f'### Global Key Metrics of {selected_country1} and {selected_country2 } in {selected_year} ')

# # Display the metrics without delta (removing the green line)
# col1, col2