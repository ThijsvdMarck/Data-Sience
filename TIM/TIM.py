#%% Importeer de benodigde bibliotheken
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
import pandas as pd
import os

def gebruik(df):
    lpg=df
    lpg['Started'] = pd.to_datetime(lpg['Started'])
    lpg['Ended'] = pd.to_datetime(lpg['Ended'])
    lpg['start_day_of_week'] = lpg['Started'].dt.day_name()
    lpg['end_day_of_week'] = lpg['Ended'].dt.day_name()

    # Maak een selectie tussen started en ended
    selectie = st.selectbox('Selecteer een optie', ['Started', 'Ended'])

    if selectie == 'Started':
        kolom = 'start_day_of_week'
    else:
        kolom = 'end_day_of_week'

    # Maak een staafgrafiek met plotly
    fig = px.bar(lpg, x=kolom, title='Frequentie van dagen in de week')
    st.plotly_chart(fig)