import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output

dfPos = pd.read_csv('posTweets.csv')
dfNeu = pd.read_csv('neuTweets.csv')
dfNeg = pd.read_csv('negTweets.csv')

app = dash.Dash(__name__)


#def main():
#    pos = 0
#   neg = 0
#    neu = 0
#    input = 22
#    for i in dfPos['hour']:
#        if i == input:
#            pos+=1
#    print(pos)
       
#if __name__ == "__main__":
#    main()

app.layout = html.Div([
   dcc.Graph(id = 'Sentiment_Analysis'),
    dcc.Slider(
        id='hour-slider',
        min=19,
        max=23,
        value=19,
        marks={str(date): str(date) for date in dfPos['hour']},
        step=None
    )
])

@app.callback(
    Output('Sentiment_Analysis', 'figure'),
    [Input('hour-slider', 'value')])

def update_figure(input_value):
    pos=0
    neg=0
    neu=0
    for i in dfPos['hour']:
        if i == input_value:
            pos+=1
    for i in dfNeg['hour']:
        if i == input_value:
            neg+=1
    for i in dfNeu['hour']:
        if i == input_value:
            neu+=1
    info = [pos,neg,neu]

    return {
        "data" : [go.Pie(labels=["Positive Tweets","Negative Tweets","Neutral Tweets"],values=info, textinfo='label')],
        "layout": go.Layout(title=f"Sentiment of Tweets regarding the South China Seas",
                        margin={"l": 300, "r": 300, },
                        legend={"x": 1, "y": 0.7})
        
    }

if __name__ == '__main__':
    app.run_server(debug=True)