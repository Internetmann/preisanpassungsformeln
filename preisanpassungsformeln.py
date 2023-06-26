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
    fix_element = st.text_input('', value='0.2', max_chars=4)

with cols[1]:
    st.subheader('Kostenelement')
    kostenelement = st.text_input('', value='0.4', max_chars=4)

with cols[2]:
    st.subheader('Marktelement')
    marktelement = st.text_input('', value='0.4', max_chars=4)

with cols[3]:
    st.subheader('Basis-Arbeitspreis')
    basis_arbeitspreis = st.text_input('', value='50', max_chars=3)

# Ensure the elements sum up to 1
total_elements = float(fix_element) + float(kostenelement) + float(marktelement)
if total_elements != 1:
    st.warning("Warning: The elements should sum up to 1.")

# Calculate the Arbeitspreis_neu
arbeitspreis_neu = float(basis_arbeitspreis) * (float(fix_element) + float(kostenelement) * gas_index / gas_index_0 +
                                               float(marktelement) * waermepreis_index / waermepreis_index_0)

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

# Display the input parameters and the plot side by side
col5, col6 = st.columns([3, 5])

with col5:
    if total_elements == 1:
        st.success("Elements sum up to 1.")
    else:
        st.warning("Warning: The elements should sum up to 1.")

with col6:
    st.plotly_chart(fig)




