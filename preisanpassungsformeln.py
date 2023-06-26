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

# Explanation text
st.markdown("Testen Sie mit diesem Tool verschiedene Preisformeln und Ihre Auswirkungen auf den Arbeitspreis. Alle Indizes sind vom Statistischen Bundesamt, die Gewichtungen müssen zusammen 1 ergeben.")

# Input widgets
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    basis_arbeitspreis = st.number_input('Basis-Arbeitspreis', min_value=20, max_value=200, step=1, value=50)

with col2:
    fix_element = st.number_input('Fix-Element', min_value=0.0, max_value=1.0, step=0.01, value=0.2)

with col3:
    marktelement = st.number_input('Wärmemarktindex (Marktelement)', min_value=0.0, max_value=1.0, step=0.01, value=0.4)

with col4:
    Erdgas_Industrie = st.number_input('Erdgas, bei Abgabe an die Industrie (Kostenelement)', min_value=0.0, max_value=1.0, step=0.01, value=0.2)

with col5:
    Erdgas_Börse = st.number_input('Erdgas, Börsennotierungen (Kostenelement)', min_value=0.0, max_value=1.0, step=0.01, value=0.2)

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
    fig.add_trace(go.Scatter(x=dates, y=arbeitspreis_neu / arbeitspreis_neu[0] * 100, name='Arbeitspreis', line=dict(color='red', width=2)))
    fig.add_trace(go.Scatter(x=dates, y=waermepreis_index / waermepreis_index_0 * 100,
                             name='Wärmepreisindex', line=dict(color='lightblue', width=2)))
    fig.add_trace(go.Scatter(x=dates, y=gas_index / gas_index_0 * 100,
                             name='Erdgas, bei Abgabe an die Industrie', line=dict(color='blue', width=2)))
    fig.add_trace(go.Scatter(x=dates, y=gas_index2 / gas_index2_0 * 100,
                             name='Erdgas, Börsennotierungen', line=dict(color='darkblue', width=2)))

    # Add the invisible dummy trace to determine the range of the primary y-axis
    dummy_trace = go.Scatter(x=dates, y=arbeitspreis_neu / arbeitspreis_neu[0] * 100,
                             showlegend=False, line=dict(color='rgba(0,0,0,0)', width=0), yaxis='y2')
    fig.add_trace(dummy_trace)

    # Calculate the range for the primary y-axis
    primary_y_range = [0, max(arbeitspreis_neu / arbeitspreis_neu[0] * 100) * 1.2]

    # Configure the first y-axis (left)
    fig.update_layout(
        yaxis=dict(
            title='Alle Reihen normiert, 01/2021 = 100',
            side='left',
            range=primary_y_range
        )
    )

    # Calculate the normalization factor
    normalization_factor = basis_arbeitspreis / 100

    # Calculate the range for the secondary y-axis
    secondary_y_range = [value * normalization_factor for value in primary_y_range]

    # Configure the second y-axis (right)
    fig.update_layout(
        yaxis2=dict(
            title='Arbeitspreis in €/MWh',
            title_font=dict(color='red'),
            side='right',
            overlaying='y',
            showgrid=False,
            tickfont=dict(color='red'),
            range=secondary_y_range,
            ticksuffix=' €/MWh'
        )
    )

    # Update the plot layout
    fig.update_layout(
        xaxis_title='Datum',
        legend=dict(
            x=0,
            y=1,
            bgcolor='rgba(255, 255, 255, 0.5)',
            orientation='v'
        ),
        autosize=True,
        margin=dict(l=20, r=20, t=60, b=20),
        showlegend=True
    )

    # Display the input parameters and the plot
    if error_message:
        st.error(error_message)
    else:
        st.plotly_chart(fig, use_container_width=True)





"""

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

# Explanation text
st.markdown("Testen Sie mit diesem Tool verschiedene Preisformeln und Ihre Auswirkungen auf den Arbeitspreis. Alle Indizes sind vom Statistischen Bundesamt, die Gewichtungen müssen zusammen 1 ergeben.")

# Input widgets
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    basis_arbeitspreis = st.number_input('Basis-Arbeitspreis', min_value=20, max_value=200, step=1, value=50)

with col2:
    fix_element = st.number_input('Fix-Element', min_value=0.0, max_value=1.0, step=0.01, value=0.2)

with col3:
    marktelement = st.number_input('Wärmemarktindex (Marktelement)', min_value=0.0, max_value=1.0, step=0.01, value=0.4)

with col4:
    Erdgas_Industrie = st.number_input('Erdgas, bei Abgabe an die Industrie (Kostenelement)', min_value=0.0, max_value=1.0, step=0.01, value=0.2)

with col5:
    Erdgas_Börse = st.number_input('Erdgas, Börsennotierungen (Kostenelement)', min_value=0.0, max_value=1.0, step=0.01, value=0.2)

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
    fig.add_trace(go.Scatter(x=dates, y=arbeitspreis_neu / arbeitspreis_neu[0] * 100, name='Arbeitspreis', line=dict(color='red', width=2)))
    fig.add_trace(go.Scatter(x=dates, y=waermepreis_index / waermepreis_index_0 * 100, name='Wärmepreisindex', line=dict(color='lightblue', width=2)))
    fig.add_trace(go.Scatter(x=dates, y=gas_index / gas_index_0 * 100, name='Erdgas, bei Abgabe an die Industrie', line=dict(color='blue', width=2)))
    fig.add_trace(go.Scatter(x=dates, y=gas_index2 / gas_index2_0 * 100, name='Erdgas, Börsennotierungen', line=dict(color='darkblue', width=2)))

    # Add the dummy trace for the secondary y-axis
    # Add the dummy trace for the secondary y-axis
    #fig.add_trace(go.Scatter(x=dates, y=arbeitspreis_neu, name='Arbeitspreis (€/MWh)', line=dict(color='rgba(0,0,0,0)', width=0), yaxis='y2'))
    # Add the invisible dummy trace to determine the range of the primary y-axis
    dummy_trace = go.Scatter(x=dates, y=arbeitspreis_neu / arbeitspreis_neu[0] * 100, showlegend=False,line=dict(color='rgba(0,0,0,0)', width=0), yaxis='y2')
    fig.add_trace(dummy_trace)

    # Calculate the range for the secondary y-axis
    primary_y_range = [0, 1200]

    
    # Configure the first y-axis (left)
    fig.update_layout(
        yaxis=dict(
            title='Alle Reihen normiert, 01/2021 = 100',
            side='left',
            range=primary_y_range
        )
    )

    # Calculate the scale factor for the second y-axis
    scale_factor = max(arbeitspreis_neu)

    # Calculate the normalization factor
    normalization_factor = basis_arbeitspreis / 100
    # Calculate the range for the secondary y-axis
    secondary_y_range = [value * normalization_factor for value in primary_y_range]
    #secondary_y_range = [value * normalization_factor for value in primary_y_range]
    #secondary_y_range = [0, max(arbeitspreis_neu / arbeitspreis_neu[0] * 100) * normalization_factor]
    # Calculate the range for the secondary y-axis
    #secondary_y_range = [min(arbeitspreis_neu) * normalization_factor, max(arbeitspreis_neu) * normalization_factor]

    # Configure the second y-axis (right)
    fig.update_layout(
        yaxis2=dict(
            title='Arbeitspreis in €/MWh',
            title_font=dict(color='red'),  # Set the title color to red
            side='right',
            overlaying='y',
            showgrid=False,
            tickfont=dict(color='red'),  # Set the tick labels to red
            range=secondary_y_range,  # Set the range based on the absolute values of Arbeitspreis
            ticksuffix=' €/MWh'  # Add the currency suffix to the tick labels
        )
    )



    # Update the plot layout
    fig.update_layout(
        xaxis_title='Datum',
        legend=dict(
            x=0,
            y=1,
            bgcolor='rgba(255, 255, 255, 0.5)',
            orientation='v'
        ),
        autosize=True,
        margin=dict(l=20, r=20, t=60, b=20),
        showlegend=True  # Show legend for all traces
    )


    # Display the input parameters and the plot
    if error_message:
        st.error(error_message)
    else:
        st.plotly_chart(fig, use_container_width=True)

"""



