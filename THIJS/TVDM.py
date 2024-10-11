#%% Importeer de benodigde bibliotheken
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
import pandas as pd
import os




def LayoutSettings():
    st.set_page_config(
        page_title="Case 3",
        page_icon="⚡",
    )
    
    st.title('Informatie over verschillende elektische ascpeten')
    st.write('Door Team 20: Tim Lind, Thijs van der Marck, Argenis de Mey, Mackenley Louis Jeune')
    st.write("""
    Op deze pagina vind je informatie over drie belangrijke onderwerpen die te maken hebben met elektrisch rijden:

    1. **Laadpaal Punten**: Alles over de locaties, beschikbaarheid en installatie van laadpalen voor elektrische voertuigen.
    2. **Laadpaal Gebruik**: Inzicht in hoe laadpalen worden gebruik en laadtijden.
    3. **Elektrische Auto's**: Informatie over de nieuwste elektrische auto's, hun prestaties, voordelen en hoe ze bijdragen aan een duurzamere toekomst.

    Verken elk onderwerp om meer te ontdekken over de toekomst van elektrisch vervoer!
    """)

def DropdownForPageSelect():

    options = ["Laadpaal Punten", "Laadpaal Gebruik", "Elektrische  Auto's"]
    page = st.selectbox('Kies een onderwerp waar u meer over wilt weten:', options)

    return page

    
def plotAantalElektrischeAutosTegenDatum(df):


    df['datum_eerste_toelating'] = pd.to_datetime(df['datum_eerste_toelating'],format="%Y%m%d")


    st.title('Elektrische Auto\'s in Nederland')


    brands = np.append('All',df['merk'].unique())

    selected_brand = st.selectbox('Kies een automerk:', brands)

    if selected_brand == 'All':
        df_filtered = df
    else:
        df_filtered = df[df['merk'] == selected_brand]


    #nog een totaal toevoegen

    df_groupby_day = df_filtered.groupby('datum_eerste_toelating').size().reset_index(name='car_count')
    df_groupby_day['cumulative_count'] = df_groupby_day['car_count'].cumsum()

    fig = px.line(df_groupby_day, 
                x='datum_eerste_toelating', 
                y='cumulative_count', 
                title='Totaal aantal extra %s elektrische Auto\'s in Nederland vanaf 2022' % selected_brand, 
                labels={
                    'datum_eerste_toelating': 'Datum', 
                    'cumulative_count': 'Aantal %s elektrische Auto\'s ' % selected_brand
                }
                )
    st.plotly_chart(fig)



    # Calculate the power-to-weight ratio
    df['power_to_weight_ratio'] = df['vermogen_massarijklaar'] / df['massa_rijklaar']

    st.title('Charging Efficiency: Power-to-Weight Ratio by Vehicle Weight')

    # Create a list of unique brands
    brands = df['merk'].unique()

    # Create a multi-select widget for brand selection, starting with no default selection
    selected_brands = st.multiselect('Select brands to display:', options=brands, default=[])

    # Filter the dataframe based on the selected brands
    df_filtered = df[df['merk'].isin(selected_brands)]

    # Only create the plot if at least one brand is selected
    if not df_filtered.empty:
        # Create the scatter plot
        fig = px.scatter(df_filtered, 
                        x='massa_rijklaar', 
                        y='power_to_weight_ratio', 
                        color='merk', 
                        title='Charging Efficiency (Power-to-Weight Ratio) by Vehicle Weight',
                        labels={'massa_rijklaar': 'Total Vehicle Mass (kg)', 'power_to_weight_ratio': 'Power-to-Weight Ratio'},
                        category_orders={'merk': selected_brands},  # Ensures the legend order matches the selected brands
                        hover_data={'handelsbenaming': True,  # Add model name (handelsbenaming) to hover info
                                    'vermogen_massarijklaar': ':.2f',  # Optionally format power to two decimal places
                                    'massa_rijklaar': True}  # Show mass in hover
                        )
        # Show the plot in Streamlit
        st.plotly_chart(fig)
    else:
        st.write("Please select at least one brand to display the chart.")
