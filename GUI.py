

import dash
from dash.html import Figure
from numpy import negative, positive
import pandas as pd 
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
from dash import Dash, dcc, html, Input, Output


df = pd.read_csv("new_file.csv")


app = dash.Dash(__name__)

app.layout = html.Div([

    html.Label(['Sentiment Analysis On Twiteer Dashboards With Dash']),
 
    dcc.Dropdown(
        id='select_OSM',
        options=[
            {'label': 'YouTube', 'value': "YouTube"},
            {'label': 'Twitter', 'value': 'sentiment'}
           
        ],
        value= 'sentiment',
         multi=False,
            clearable=False,
            style={"width": "50%"}
    ),
    html.Div([
        dcc.Graph(id='Sentiment_Analysis'),
]),

])


@app.callback(

   Output(component_id='Sentiment_Analysis', component_property='figure'),
    [Input(component_id='select_OSM', component_property='value')]
)
def update_graph(select_OSM):
    dff = df

    pie_graph = px.pie(data_frame=dff, names=select_OSM, hole=.3,)
    return(pie_graph)

if __name__ == '__main__':
    app.run_server(debug=True)