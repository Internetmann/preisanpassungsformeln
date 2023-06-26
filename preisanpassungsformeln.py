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
st.sidebar.header('Input Parameters')

# Input widgets
fix_element = st.sidebar.number_input('Fix-Element', min_value=0.0, max_value=1.0, step=0.01, value=0.2)
kostenelement = st.sidebar.number_input('Kostenelement', min_value=0.0, max_value=1.0, step=0.01, value=0.4)
marktelement = st.sidebar.number_input('Marktelement', min_value=0.0, max_value=1.0, step=0.01, value=0.4)
basis_arbeitspreis = st.sidebar.number_input('Basis-Arbeitspreis', min_value=20, max_value=200, step=1, value=50)

# Ensure the elements sum up to 1
total_elements = fix_element + kostenelement + marktelement
if total_elements != 1:
    st.warning("Warning: The elements should sum up to 1.")

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

# Display the plot
st.plotly_chart(fig)

# Provide feedback
if total_elements == 1:
    st.success("Elements sum up to 1.")
