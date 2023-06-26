#!pip install streamlit

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Load the data from the Excel file
data = pd.read_excel('widget_data.xlsx')

# Extract the relevant columns from the data
gas_index_0 = data['Erdgas, bei Abgabe an die Industrie'][0]
waermepreis_index_0 = data['Wärmepreisindex'][0]
dates = data['Datum']
gas_index = data['Erdgas, bei Abgabe an die Industrie']
waermepreis_index = data['Wärmepreisindex']

# Set up the layout
st.title('Fernwärme Arbeitspreisanpassung')

# Input widgets
cols = st.columns(4)

with cols[0]:
    st.subheader('Fix-Element')
    fix_element = st.number_input('Fix-Element', min_value=0.0, max_value=1.0, step=0.01, value=0.2)

with cols[1]:
    st.subheader('Kostenelement')
    kostenelement = st.number_input('Kostenelement', min_value=0.0, max_value=1.0, step=0.01, value=0.4)

with cols[2]:
    st.subheader('Marktelement')
    marktelement = st.number_input('Marktelement', min_value=0.0, max_value=1.0, step=0.01, value=0.4)

with cols[3]:
    st.subheader('Basis-Arbeitspreis')
    basis_arbeitspreis = st.number_input('Basis-Arbeitspreis', min_value=20, max_value=200, step=1, value=50)

# Ensure the elements sum up to 1
total_elements = fix_element + kostenelement + marktelement
if total_elements != 1:
    error_message = f"Die Gewichtungen ergeben {total_elements:.2f} statt 1."
else:
    error_message = ""

# Create the plot if there is no error
if not error_message:
    # Calculate the Arbeitspreis_neu
    arbeitspreis_neu = basis_arbeitspreis * (fix_element + kostenelement * gas_index / gas_index_0 +
                                             marktelement * waermepreis_index / waermepreis_index_0)

    # Create the plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=arbeitspreis_neu, name='Arbeitspreis_neu'))
    fig.add_trace(go.Scatter(x=dates, y=gas_index, name='Gasindex'))
    fig.add_trace(go.Scatter(x=dates, y=waermepreis_index, name='Wärmepreisindex'))

    # Update the plot layout
    fig.update_layout(
        title='Fernwärme Arbeitspreisanpassung',
        xaxis_title='Datum',
        yaxis_title='Preis',
        legend_title='Kategorie',
    )

# Display the input parameters and the plot/error message
col1, col2 = st.columns([4, 8])

with col1:
    if error_message:
        st.error(error_message)

with col2:
    if error_message:
        st.write("Please fix the input parameters.")
    else:
        st.plotly_chart(fig, use_container_width=True)










