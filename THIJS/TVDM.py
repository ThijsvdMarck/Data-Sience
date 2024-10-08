#%% Importeer de benodigde bibliotheken
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
import pandas as pd
import os

def THIJS(a,b):
    df1 = a
    df2 = b



    return print('THIJS\n',a+b)

def plot(df):
    df = df

    # st.title('LOLOLOL')
    # fig = px.line(df, x='DateLastVerified', y='IsRecentlyVerified')
    # fig.update_xaxes(dtick=10)
    # st.plotly_chart(fig)

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