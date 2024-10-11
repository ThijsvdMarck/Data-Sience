#%% Importeer de benodigde bibliotheken
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
import pandas as pd
import os
import plotly.graph_objects as go

def gebruik(df):
    lpg = df
    lpg = lpg[(lpg['ConnectedTime'] <= 24) & (lpg['ConnectedTime'] >= 0.1) & (lpg['ConnectedTime'] >= lpg['ChargeTime']) & (lpg['ChargeTime'] > 0)]
    lpg['Started'] = pd.to_datetime(lpg['Started'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
    lpg['Ended'] = pd.to_datetime(lpg['Ended'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
    lpg['Started'] = pd.to_datetime(lpg['Started'])
    lpg['Ended'] = pd.to_datetime(lpg['Ended'])
    lpg['start_day_of_week'] = lpg['Started'].dt.day_name()
    lpg['end_day_of_week'] = lpg['Ended'].dt.day_name()

    # Create new columns for Started
    lpg['Started_Monday'] = np.where(lpg['start_day_of_week'] == 'Monday', lpg['Started'].dt.hour + lpg['Started'].dt.minute / 60, np.nan)
    lpg['Started_Tuesday'] = np.where(lpg['start_day_of_week'] == 'Tuesday', lpg['Started'].dt.hour + lpg['Started'].dt.minute / 60, np.nan)
    lpg['Started_Wednesday'] = np.where(lpg['start_day_of_week'] == 'Wednesday', lpg['Started'].dt.hour + lpg['Started'].dt.minute / 60, np.nan)
    lpg['Started_Thursday'] = np.where(lpg['start_day_of_week'] == 'Thursday', lpg['Started'].dt.hour + lpg['Started'].dt.minute / 60, np.nan)
    lpg['Started_Friday'] = np.where(lpg['start_day_of_week'] == 'Friday', lpg['Started'].dt.hour + lpg['Started'].dt.minute / 60, np.nan)
    lpg['Started_Saturday'] = np.where(lpg['start_day_of_week'] == 'Saturday', lpg['Started'].dt.hour + lpg['Started'].dt.minute / 60, np.nan)
    lpg['Started_Sunday'] = np.where(lpg['start_day_of_week'] == 'Sunday', lpg['Started'].dt.hour + lpg['Started'].dt.minute / 60, np.nan)

    # Create new columns for Ended
    lpg['Ended_Monday'] = np.where(lpg['end_day_of_week'] == 'Monday', lpg['Ended'].dt.hour + lpg['Ended'].dt.minute / 60, np.nan)
    lpg['Ended_Tuesday'] = np.where(lpg['end_day_of_week'] == 'Tuesday', lpg['Ended'].dt.hour + lpg['Ended'].dt.minute / 60, np.nan)
    lpg['Ended_Wednesday'] = np.where(lpg['end_day_of_week'] == 'Wednesday', lpg['Ended'].dt.hour + lpg['Ended'].dt.minute / 60, np.nan)
    lpg['Ended_Thursday'] = np.where(lpg['end_day_of_week'] == 'Thursday', lpg['Ended'].dt.hour + lpg['Ended'].dt.minute / 60, np.nan)
    lpg['Ended_Friday'] = np.where(lpg['end_day_of_week'] == 'Friday', lpg['Ended'].dt.hour + lpg['Ended'].dt.minute / 60, np.nan)
    lpg['Ended_Saturday'] = np.where(lpg['end_day_of_week'] == 'Saturday', lpg['Ended'].dt.hour + lpg['Ended'].dt.minute / 60, np.nan)
    lpg['Ended_Sunday'] = np.where(lpg['end_day_of_week'] == 'Sunday', lpg['Ended'].dt.hour + lpg['Ended'].dt.minute / 60, np.nan)

    # Maak een selectie tussen started en ended
    selectie = st.selectbox('Select an option for the y-as', ['Car is plugged in', 'Car is plugged out'])

    # Maak een selectie voor de x-as
    x_as_selectie = st.selectbox('Select an option for the x-as', ['Days', 'Hours'])

    if selectie == 'Car is plugged in':
        if x_as_selectie == 'Days':
            kolom = 'start_day_of_week'
        else:
            day_selectie = st.multiselect('Select one or multiple days', ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
            if day_selectie:
                kolommen = [f'Started_{dag}' for dag in day_selectie]
                lpg['Started_Uren'] = lpg[kolommen].stack().reset_index(level=1, drop=True)
                kolom = 'Started_Uren'
            else:
                kolom = 'Started_Monday'
    else :
        if x_as_selectie == 'Days':
            kolom = 'end_day_of_week'
        else:
            day_selectie = st.multiselect('Select one or multiple days', ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
            if day_selectie:
                kolommen = [f'Ended_{dag}' for dag in day_selectie]
                lpg['Ended_Uren'] = lpg[kolommen].stack().reset_index(level=1, drop=True)
                kolom = 'Ended_Uren'
            else:
                kolom = 'Ended_Monday'

    # Maak een staafgrafiek met plotly
    if x_as_selectie == 'Hours':
        lpg[kolom] = lpg[kolom].round(0)
        freq = lpg[kolom].value_counts().sort_index()
        if day_selectie:
            title = f'Frequention of hours on {", ".join(day_selectie)}'
        else:
            title = f'Frequention of hours'
        fig = px.bar(x=freq.index, y=freq.values, title=title)
        fig.update_layout(xaxis_title='Hour of the Day', yaxis_title='Frequency')
        fig.update_xaxes(dtick=1)  # show all hours on the x-axis
    else:
        fig = px.bar(lpg, x=kolom, title='Frequentie van dagen in de week')
        fig.update_layout(xaxis_title='Days of the week', yaxis_title='Frequency')
    st.plotly_chart(fig)

    # New plot for ConnectedTime and ChargeTime
    new_selectie = st.multiselect('Select one or multiple options for the new plot', ['ConnectedTime', 'ChargeTime'])

    # Use the same x-as selection for fig2 as fig1
    if x_as_selectie == 'Days':
        new_kolom = 'start_day_of_week'
        if 'ConnectedTime' in new_selectie:
            connected_time_avg = lpg.groupby(new_kolom)['ConnectedTime'].mean()
        if 'ChargeTime' in new_selectie:
            charge_time_avg = lpg.groupby(new_kolom)['ChargeTime'].mean()

        fig2 = go.Figure()
        if 'ConnectedTime' in new_selectie:
            fig2.add_trace(go.Bar(x=connected_time_avg.index, y=connected_time_avg.values, name='Connected Time', marker_color='blue'))
        if 'ChargeTime' in new_selectie:
            fig2.add_trace(go.Bar(x=charge_time_avg.index, y=charge_time_avg.values, name='Charge Time', marker_color='red'))

        fig2.update_layout(xaxis_title='Days of the week', yaxis_title='Average Time', barmode='group')
        st.plotly_chart(fig2)
    else:
        new_day_selectie = day_selectie  # use the same day selection as fig1
        if new_day_selectie:
            new_kolommen = [f'Started_{dag}' for dag in new_day_selectie]
            lpg['Started_Uren_new'] = lpg[new_kolommen].stack().reset_index(level=1, drop=True)
            new_kolom = 'Started_Uren_new'
        else:
            new_kolom = 'Started_Monday'

        # Bereken het gemiddelde per uur
        uren = np.arange(1, 25)  # array met uren van 1 tot 24
        if 'ConnectedTime' in new_selectie:
            connected_time_avg = [lpg[lpg[new_kolom].round(1) == uur]['ConnectedTime'].mean() for uur in uren]
        if 'ChargeTime' in new_selectie:
            charge_time_avg = [lpg[lpg[new_kolom].round(1) == uur]['ChargeTime'].mean() for uur in uren]

        fig2 = go.Figure()
        if 'ConnectedTime' in new_selectie:
            fig2.add_trace(go.Bar(x=uren, y=connected_time_avg, name='Connected Time', marker_color='blue'))
        if 'ChargeTime' in new_selectie:
            fig2.add_trace(go.Bar(x=uren, y=charge_time_avg, name='Charge Time', marker_color='red'))

        if fig2 is not None:
            fig2.update_layout(xaxis_title='Hour of the Day', yaxis_title='Average Time', barmode='group')
            fig2.update_xaxes(dtick=1, tick0=1, tickmode='linear')
            st.plotly_chart(fig2)