# # -*- coding: utf-8 -*-
# Case 2 Team 20 - Thijs van der Marck, Rob van der Vaart, Jelle van der Wal

#%% Importeer de benodigde bibliotheken
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
import kaggle as kg
import pandas as pd
import os

import TVDM as tv


tv.THIJS(1,1)



#%% Load Kaggle API data
os.environ['KAGGLE_USERNAME'] = 'thijsvandermarck'
os.environ['KAGGLE_KEY'] = '07f3e809702e7b2b43e9e7d4858933f1'
 
kg.api.authenticate()
 
kg.api.dataset_download_files(dataset = "moazzimalibhatti/co2-emission-by-countries-year-wise-17502022", path='on.zip', unzip=True)
 
df = pd.read_csv('on.zip/CO2 emission by countries.csv', encoding='ISO-8859-1')

# Lees het bestand 'CO2 emission by countries.csv' in als een dataframe.
# df = pd.read_csv('CO2 emission by countries.csv', encoding='latin1')
# print(df.info())
# print(df.head())

#%% Data inventariseren & schoonmaken
# Zoek alle ontbrekende waarden in de dataframe
missing_values = df.isna().sum()
print(missing_values)

# Omdat de kolom 'Code' en 'Calling Code' ontbrekende waarden bevat en niet relevant zijn, verwijderen we deze kolom
df.drop('Code', axis=1, inplace=True)
df.drop('Calling Code', axis=1, inplace=True)

# % of World en Density(km2) zijn Dtype objest, deze kunnen we veranderen in float.
df['Density(km2)'] = df['Density(km2)'].str.replace('/km²', '')
df['Density(km2)'] = df['Density(km2)'].str.replace(',', '.').astype(float)
df['% of World'] = df['% of World'].str.replace('%', '').astype(float)
df['Year'] = df['Year'].astype(float)

# Om te zien bij welke landen er waardes ontbreken.
columns_with_no_value = df.columns[df.isna().any()]
country_density_means = df.groupby('Country')[columns_with_no_value].mean()
countries_with_nan_in_every_column = country_density_means.index[country_density_means.isna().all(axis=1)]
print(countries_with_nan_in_every_column)

# Verwijder deze landen.
df = df[df['Country'].isin(countries_with_nan_in_every_column) == False]

# Zoek alle ontbrekende waarden in de dataframe in procent.
missing_values = df.isna().sum()
df_lenght = len(df)
missing_values_percentage = missing_values / df_lenght * 100
print(missing_values_percentage)

# Verwijder de rijen in de kolommen waar er 5% of minder waardes ontbreken.
threshold=len(df)*0.05
rows_to_drop=df.columns[df.isna().sum()  <= threshold]
df.dropna(subset=rows_to_drop, inplace=True)

#%% Extra statistiek maken
# Bereken $ of World met de Area
total_land_area=144500000
df['% of World'] = round((df['Area']/total_land_area) * 100,4)

# CO2 per jaar.
df = df.sort_values(by=['Country', 'Year'])
df['CO2 emission (Tons)'] = df.groupby('Country')['CO2 emission (Tons)'].diff()
df['CO2 emission (Tons)'].fillna(0, inplace=True)

# Tweede dataset toevoegen om population per jaar (1960-2020) te krijgen. 
df2 = pd.read_csv('c:/Users/robva/Downloads/World-population-by-countries-dataset.csv', encoding='latin1')

# Verwijder de rijen in de kolommen waar er 5% of minder waardes ontbreken.
threshold2=len(df2)*0.05
rows_to_drop2=df2.columns[df2.isna().sum()  <= threshold2]
df2.dropna(subset=rows_to_drop2, inplace=True)

# Omdat de kolom 'Country Code' niet relevant zijn, verwijderen we deze kolom.
df2.drop('Country Code', axis=1, inplace=True)

# Geef df2 dezelfde layout als df
df2_melted = pd.melt(df2, id_vars=['Country Name'], var_name='Year', value_name='Population')
df2_melted['Year'] = df2_melted['Year'].astype(int)
df2_melted = df2_melted.sort_values(['Country Name', 'Year'])
df2_melted = df2_melted.reset_index(drop=True)
print(df2_melted.head()) 

merged_df = pd.merge(df, df2_melted, left_on=['Country', 'Year'], right_on=['Country Name', 'Year'])
merged_df.loc[:, 'Population(2022)'] = merged_df.loc[:, 'Population']

# Dubbele Country Name verwijderen.
merged_df.drop('Country Name', axis=1, inplace=True)

# Omdat Density(km2) en Population(2022) niet per jaar zijn, verwijderen we deze ook.
merged_df.drop('Density(km2)', axis=1, inplace=True)
merged_df.drop('Population(2022)', axis=1, inplace=True)

# Inwoners dichtheid toevoegen in /kg^2
merged_df['Population Density'] = merged_df['Population'] / merged_df['Area']
print(merged_df[merged_df['Country']=="Netherlands"].head(10))

#%%__________________________________________________________________________________
#%% Streamlit

#%% Eerst plot
# Streamlit UI opzetten
st.title('CO2 Emissions per Country')

# Landen in dropdown selecteren 
countries = df['Country'].unique()
selected_country = st.selectbox('Select a country', countries)
country_data = df[df['Country'] == selected_country]

# Groepeer de data per jaar en maak lineplot met plotly voor CO2 emission
country_data_groupby = country_data.groupby('Year')['CO2 emission (Tons)'].sum().reset_index()
country_data_groupby_non_zero = country_data_groupby[country_data_groupby['CO2 emission (Tons)'] > 0]
    
tv.plot(df)

#%% Tweede plot met twee landen vergelijking
# Streamlit UI opzetten
st.title('Comparing CO2 statistics of two countries')

# Maak een dropdown om tussen CO2 en CO2 per capita te wisselen
plot_type = st.selectbox('Select plot type', ['CO2 Emissions per Capita','Comparing CO2 Emissions per km²']) #, 'Comparing CO2 Emissions% per km²

# Landen in dropdown selecteren 
countries = merged_df['Country'].unique()

# Selecteer twee landen
selected_country1 = st.selectbox('Select country 1', countries)
selected_country2 = st.selectbox('Select country 2', countries)

# Data voor de twee landen
country_data1 = merged_df[merged_df['Country'] == selected_country1]
country_data2 = merged_df[merged_df['Country'] == selected_country2]

# Voor de eerste plot
country_data1_groupby = country_data1.groupby('Year')[['Population', 'CO2 emission (Tons)']].sum().reset_index()
country_data1_groupby['Population_per_CO2'] = country_data1_groupby['CO2 emission (Tons)'] / country_data1_groupby['Population']

country_data2_groupby = country_data2.groupby('Year')[['Population', 'CO2 emission (Tons)']].sum().reset_index()
country_data2_groupby['Population_per_CO2'] = country_data2_groupby['CO2 emission (Tons)'] / country_data2_groupby['Population']

country_data1_groupby_non_zero = country_data1_groupby[country_data1_groupby['CO2 emission (Tons)'] > 0]
country_data2_groupby_non_zero = country_data2_groupby[country_data2_groupby['CO2 emission (Tons)'] > 0]

# Voor de tweede plot

country_data3_groupby = country_data1.groupby('Year')[['Area', 'CO2 emission (Tons)']].sum().reset_index()
country_data3_groupby['Area_per_CO2'] = (country_data3_groupby['CO2 emission (Tons)'] / country_data3_groupby['Area'])

country_data4_groupby = country_data2.groupby('Year')[['Area', 'CO2 emission (Tons)']].sum().reset_index()
country_data4_groupby['Area_per_CO2'] = (country_data4_groupby['CO2 emission (Tons)'] / country_data4_groupby['Area'])

country_data3_groupby_non_zero = country_data3_groupby[country_data3_groupby['CO2 emission (Tons)'] > 0]
country_data4_groupby_non_zero = country_data4_groupby[country_data3_groupby['CO2 emission (Tons)'] > 0]

# #Derde plot ZIT EEN REKENFOUT IN
# merged_df['CO2 emission (%)'] = 0.0

# # Iterate over each unique year
# for year in merged_df['Year'].unique():
#     # Filter data for the specific year
#     year_data = merged_df[merged_df['Year'] == year]
        
#     # Calculate the total CO2 emissions for the year
#     total_emission = year_data['CO2 emission (Tons)'].sum()
        
#     # Calculate the percentage for each country and update the 'CO2 emission (%)' column
#     merged_df.loc[merged_df['Year'] == year, 'CO2 emission (%)'] = (merged_df.loc[merged_df['Year'] == year, 'CO2 emission (Tons)'] / total_emission) * 100


# # Data voor de twee landen
# country_data_d = merged_df[merged_df['Country'] == selected_country1]
# country_data_e = merged_df[merged_df['Country'] == selected_country1]

# # Groepeer de data per jaar en maak lineplot met plotly voor CO2 emission %
# country_data_d_groupby = country_data_d.groupby('Year')[['Area', 'CO2 emission (%)']].sum().reset_index()
# country_data_d_groupby['Area_per_CO2%'] = (country_data_d_groupby['CO2 emission (%)'] / country_data_d_groupby['Area'])

# country_data_e_groupby = country_data_e.groupby('Year')[['Area', 'CO2 emission (%)']].sum().reset_index()
# country_data_e_groupby['Area_per_CO2%'] = (country_data_e_groupby['CO2 emission (%)'] / country_data_e_groupby['Area'])

# country_data_d_groupby_non_zero = country_data_d_groupby[country_data_e_groupby['CO2 emission (%)'] > 0]
# country_data_e_groupby_non_zero = country_data_e_groupby[country_data_d_groupby['CO2 emission (%)'] > 0]

# Conditie om te kiezen welk plot te tonen
if plot_type == 'CO2 Emissions per Capita':

    fig = px.line(country_data_groupby_non_zero, x='Year', y='CO2 emission (Tons)', title=f'CO2 Emissions in {selected_country} per year')
    fig.update_yaxes(range=[0, country_data_groupby['CO2 emission (Tons)'].max()])

    # Maak een enkele lineplot voor de twee landen
    fig = px.line()
    fig.add_scatter(x=country_data1_groupby_non_zero['Year'], y=country_data1_groupby_non_zero['Population_per_CO2'], name=selected_country1)
    fig.add_scatter(x=country_data2_groupby_non_zero['Year'], y=country_data2_groupby_non_zero['Population_per_CO2'], name=selected_country2)
    fig.update_xaxes(dtick=10)
    fig.update_yaxes(range=[0, max(country_data1_groupby['Population_per_CO2'].max(), country_data2_groupby['Population_per_CO2'].max())])
    fig.update_layout(
        title=f'Amount of CO2 Emissions in {selected_country1} and {selected_country2} per year, per capita',
        xaxis_title='Year',
        yaxis_title='Population per CO2 (tons)'
    )
    st.plotly_chart(fig)
elif plot_type == 'Comparing CO2 Emissions per km²':
    # Maak een enkele lineplot voor de twee landen
    fig3 = px.line()
    fig3.add_scatter(
        x=country_data3_groupby_non_zero['Year'],
        y=country_data3_groupby_non_zero['Area_per_CO2'],
        name=selected_country1
    )
    fig3.add_scatter(
        x=country_data4_groupby_non_zero['Year'],
        y=country_data4_groupby_non_zero['Area_per_CO2'],
        name=selected_country2
    )
    fig3.update_xaxes(dtick=10)
    fig3.update_yaxes(range=[
        0,
        max(
            country_data3_groupby['Area_per_CO2'].max(),
            country_data4_groupby['Area_per_CO2'].max()
        )
    ])
    fig3.update_layout(
        title=f'Amount of CO2 Emissions in {selected_country1} and {selected_country2} per year, per km²',
        xaxis_title='Year',
        yaxis_title='CO2 (tons) per km²'
    )
    st.plotly_chart(fig3)
# else: ZIT EEN REKENFOUT IN

#     # Maak een enkele lineplot voor de twee landen
#     fig4 = px.line()
#     fig4.add_scatter(x=country_data_e_groupby_non_zero['Year'], y=country_data_e_groupby_non_zero['Area_per_CO2%'], name=selected_country1)
#     fig4.add_scatter(x=country_data_d_groupby_non_zero['Year'], y=country_data_d_groupby_non_zero['Area_per_CO2%'], name=selected_country2)
#     fig4.update_xaxes(dtick=10)
#     fig4.update_yaxes(range=[0, max(country_data_d_groupby['Area_per_CO2%'].max(), country_data_e_groupby['Area_per_CO2%'].max())])
#     fig4.update_layout(
#         title=f'Amount of CO2 Emissions Percentage in {selected_country1} and {selected_country2} per year, per km²',
#         xaxis_title='Year',
#         yaxis_title='CO2% per km²'
#     )
#     st.plotly_chart(fig4)
#%% Stats onderaan
# Selecteer een jaar.
selected_year = st.selectbox('Select year', [int(year) for year in merged_df['Year'].unique()])
 
# Data voor de twee landen in het geselecteerde jaar
country_data1_year = country_data1[country_data1['Year'] == selected_year]
country_data2_year = country_data2[country_data2['Year'] == selected_year]
 
# Bereken de percentages
global_co2_emission = merged_df[merged_df['Year'] == selected_year]['CO2 emission (Tons)'].sum()
global_population = merged_df[merged_df['Year'] == selected_year]['Population'].sum()
 
co2_emission_percentage_country1 = round((country_data1_year['CO2 emission (Tons)'].sum() / global_co2_emission) * 100,3)
co2_emission_percentage_country2 = round((country_data2_year['CO2 emission (Tons)'].sum() / global_co2_emission) * 100,3)
 
population_percentage_country1 = round((country_data1_year['Population'].sum() / global_population) * 100,3)
population_percentage_country2 = round((country_data2_year['Population'].sum() / global_population) * 100,3)
 
# Weergeef de percentages onder de grafiek
st.write(f'### Global Key Metrics of {selected_country1} and {selected_country2 } in {selected_year} ')

# Display the metrics without delta (removing the green line)
col1, col2 = st.columns(2)

with col1:
    st.metric(
        label=f'{selected_country1} CO2 Emissions',
        value=f'{co2_emission_percentage_country1}%',
        delta=None  # No delta, so no green/red line
    )
    st.metric(
        label=f'{selected_country1} Population',
        value=f'{population_percentage_country1}%',
        delta=None  # No delta, so no green/red line
    )

with col2:
    st.metric(
        label=f'{selected_country2} CO2 Emissions',
        value=f'{co2_emission_percentage_country2}%',
        delta=None  # No delta, so no green/red line
    )
    st.metric(
        label=f'{selected_country2} Population',
        value=f'{population_percentage_country2}%',
        delta=None  # No delta, so no green/red line
    )