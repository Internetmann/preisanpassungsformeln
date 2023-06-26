#pip install dash

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd

# Load the data from the Excel file
github_url = 'https://raw.githubusercontent.com/Internetmann/preisanpassungsformeln/main/widget_data.xlsx'
data = pd.read_excel(github_url)

# Extract the relevant columns from the data
gas_index_0 = data['Erdgas, bei Abgabe an die Industrie'][0]
waermepreis_index_0 = data['Wärmepreisindex'][0]
dates = data['Datum']
gas_index = data['Erdgas, bei Abgabe an die Industrie']
waermepreis_index = data['Wärmepreisindex']

# Create the Dash app
app = dash.Dash(__name__)

# Set up the layout
app.layout = html.Div([
    html.H1('Fernwärme Arbeitspreisanpassung'),
    html.Div([
        html.Label('Fix-Element'),
        dcc.Input(id='fix-element-input', type='number', min=0, max=1, step=0.01, value=0.2),
        html.Label('Kostenelement'),
        dcc.Input(id='kostenelement-input', type='number', min=0, max=1, step=0.01, value=0.4),
        html.Label('Marktelement'),
        dcc.Input(id='marktelement-input', type='number', min=0, max=1, step=0.01, value=0.4),
        html.Label('Basis-Arbeitspreis'),
        dcc.Input(id='basis-arbeitspreis-input', type='number', min=20, max=200, step=1, value=50),
        html.Div(id='feedback-div')
    ]),
    dcc.Graph(id='output-plot')
])

@app.callback(
    Output('output-plot', 'figure'),
    Output('feedback-div', 'children'),
    Input('fix-element-input', 'value'),
    Input('kostenelement-input', 'value'),
    Input('marktelement-input', 'value'),
    Input('basis-arbeitspreis-input', 'value')
)
def update_plot(fix_element, kostenelement, marktelement, basis_arbeitspreis):
    # Ensure the elements sum up to 1
    total_elements = fix_element + kostenelement + marktelement
    if total_elements != 1:
        feedback = html.Span("Warning: The elements should sum up to 1.", style={'color': 'red'})
        return go.Figure(), feedback

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

    # Provide feedback
    feedback = html.Span("Elements sum up to 1.", style={'color': 'green'})

    return fig, feedback

if __name__ == "__main__":
    app.run_server(debug=True)
