import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

pio.renderers.default = 'browser'

df = pd.read_csv('forFBpost.csv', sep=';')
df.columns = ['city', 'year', 'fact', 'model', 'low_limit', 'high_limit']
df = df[df['city'] != 'Москва']

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# ***LAYOUT***

app.layout = html.Div([
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                df['city'].unique(),
                'Select city from list',
                id='city-name'
            )
        ], width={'size':4})
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='graphic')
        ], width={'size':6})
    ])
])

@app.callback(
    Output('graphic', 'figure'),
    Input('city-name', 'value'))
def update_graph(city_name):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df[df['city'] == city_name]['year'],
                             y=df[df['city'] == city_name]['model'],
                             mode='lines', name='model'))
    fig.add_trace(go.Scatter(x=df[df['city'] == city_name]['year'],
                             y=df[df['city'] == city_name]['high_limit'],
                             mode='lines', name='high limit'))
    fig.add_trace(go.Scatter(x=df[df['city'] == city_name]['year'],
                             y=df[df['city'] == city_name]['low_limit'],
                             mode='lines', name='low limit'))
    fig.add_trace(go.Scatter(x=df[df['city'] == city_name]['year'],
                             y=df[df['city'] == city_name]['fact'],
                             opacity=0.75,
                             mode='markers', name='fact'))
    fig.update_traces(marker=dict(size=8,
                                  symbol='diamond',
                                  line=dict(width=1,
                                            color='DarkSlateGrey')),
                      selector=dict(mode='markers'))
    fig.update_layout(title="Cities dashboard",
                      xaxis_title="Years",
                      yaxis_title="Population",
                      )

    # fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
