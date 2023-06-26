import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Load the data from the Excel file
data = pd.read_excel('widget_data2.xlsx')

# Extract the relevant columns from the data
gas_index_0 = data['Erdgas, bei Abgabe an die Industrie'][0]
gas_index2_0 = data['Erdgas, Börsennotierungen'][0]
waermepreis_index_0 = data['Wärmepreisindex'][0]
dates = data['Datum']
gas_index = data['Erdgas, bei Abgabe an die Industrie']
gas_index2 = data['Erdgas, Börsennotierungen']
waermepreis_index = data['Wärmepreisindex']

# Set up the layout
st.title('Fernwärme Arbeitspreisanpassung')

# Input widgets
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    fix_element = st.number_input('Fix-Element', min_value=0.0, max_value=1.0, step=0.01, value=0.2)

with col2:
    Erdgas_Industrie = st.number_input('Erdgas, bei Abgabe an die Industrie', min_value=0.0, max_value=1.0, step=0.01, value=0.2)

with col3:
    marktelement = st.number_input('Marktelement', min_value=0.0, max_value=1.0, step=0.01, value=0.4)

with col4:
    basis_arbeitspreis = st.number_input('Basis-Arbeitspreis', min_value=20, max_value=200, step=1, value=50)

with col5:
    Erdgas_Börse = st.number_input('Erdgas, Börsennotierungen', min_value=0.0, max_value=1.0, step=0.01, value=0.2)

# Ensure the elements sum up to 1
total_elements = fix_element + Erdgas_Industrie + marktelement + Erdgas_Börse
if total_elements != 1:
    error_message = f"Vorsicht: Die Gewichtungen ergeben zusammen {total_elements:.2f} statt 1."
else:
    error_message = ""

# Create the plot if there is no error
if not error_message:
    # Calculate the Arbeitspreis_neu
    arbeitspreis_neu = basis_arbeitspreis * (fix_element + 
                                             Erdgas_Industrie * gas_index / gas_index_0 +
                                             marktelement * waermepreis_index / waermepreis_index_0 +
                                             Erdgas_Börse * gas_index2 / gas_index2_0)

    # Create the plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=arbeitspreis_neu, name='Arbeitspreis', line=dict(color='red', width=2)))
    fig.add_trace(go.Scatter(x=dates, y=gas_index, name='Erdgas, bei Abgabe an die Industrie', line=dict(color='blue', width=2)))
    fig.add_trace(go.Scatter(x=dates, y=waermepreis_index, name='Wärmepreisindex', line=dict(color='green', width=2)))
    fig.add_trace(go.Scatter(x=dates, y=gas_index2, name='Erdgas, Börsennotierungen', line=dict(color='orange', width=2)))

    # Update the plot layout
    fig.update_layout(
        xaxis_title='Datum',
        yaxis_title='Preis',
        legend=dict(
            x=0,
            y=1,
            bgcolor='rgba(255, 255, 255, 0.5)',
            orientation='v'
        ),
        autosize=True,
        margin=dict(l=20, r=20, t=60, b=20)
    )

# Display the input parameters
if error_message:
    st.error(error_message)
else:
    st.plotly_chart(fig, use_container_width=True)



'''

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
col1, col2, col3, col4 = st.columns(4)

with col1:
    fix_element = st.number_input('Fix-Element', min_value=0.0, max_value=1.0, step=0.01, value=0.2)

with col2:
    kostenelement = st.number_input('Kostenelement', min_value=0.0, max_value=1.0, step=0.01, value=0.4)

with col3:
    marktelement = st.number_input('Marktelement', min_value=0.0, max_value=1.0, step=0.01, value=0.4)

with col4:
    basis_arbeitspreis = st.number_input('Basis-Arbeitspreis', min_value=20, max_value=200, step=1, value=50)

# Ensure the elements sum up to 1
total_elements = fix_element + kostenelement + marktelement
if total_elements != 1:
    error_message = f"Vorsicht: Die Gewichtungen ergeben zusammen {total_elements:.2f} statt 1."
else:
    error_message = ""

# Create the plot if there is no error
if not error_message:
    # Calculate the Arbeitspreis_neu
    arbeitspreis_neu = basis_arbeitspreis * (fix_element + kostenelement * gas_index / gas_index_0 +
                                             marktelement * waermepreis_index / waermepreis_index_0)

    # Create the plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=arbeitspreis_neu, name='Arbeitspreis', line=dict(color='red', width=2)))
    fig.add_trace(go.Scatter(x=dates, y=gas_index, name='Erdgas, bei Abgabe an die Industrie', line=dict(color='blue', width=2)))
    fig.add_trace(go.Scatter(x=dates, y=waermepreis_index, name='Wärmepreisindex', line=dict(color='green', width=2)))

    # Update the plot layout
    fig.update_layout(
        xaxis_title='Datum',
        yaxis_title='Preis',
        legend=dict(
            x=0,
            y=1,
            bgcolor='rgba(255, 255, 255, 0.5)',
            orientation='v'
        ),
        autosize=True,
        margin=dict(l=20, r=20, t=60, b=20)
    )

# Display the input parameters
if error_message:
    st.error(error_message)
else:
    st.plotly_chart(fig, use_container_width=True)











