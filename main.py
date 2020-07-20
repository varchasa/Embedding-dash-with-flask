from flask import Flask, render_template,url_for,request,send_file
import pandas as pd
import matplotlib.pyplot as plt
import csv
from flask_mysqldb import MySQL
import yaml
import plotly
import plotly.express as px
import plotly.graph_objects as obj
import dash             
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

server = Flask(__name__)
mysql = MySQL(server)


app1 = dash.Dash(__name__,server=server,url_base_pathname='/tweets/' )
data = pd.read_csv('corona_tweets_01.csv')

fig1=obj.Figure(obj.Scattergl(x=data['tweet_id'][0:2000],
	y=data['sentiment'][0:2000],
	mode = 'markers'))

fig2 = obj.Figure(obj.Scattergl(x=data['tweet_id'][2000:10000],
	y=data['sentiment'][2000:10000],
	mode = 'markers'))

fig3=obj.Figure(obj.Scattergl(x=data['tweet_id'][10000:40000],
	y=data['sentiment'][10000:40000],
	mode = 'markers'))

app1.layout = html.Div(children = [
    html.H1(children = 'Analysis of covid-19 first 2000 tweets'), html.Hr(),
    dcc.Graph(
    	figure=fig1),
    html.H1(children = 'Analysis of covid-19 next 10000 tweets'), html.Hr(),
    dcc.Graph(
    	figure=fig2),
    html.H1(children = 'Analysis of covid-19 next 40000 tweets'), html.Hr(),
    dcc.Graph(
    	figure=fig3)
])

app = dash.Dash(__name__,server=server,url_base_pathname='/dashboard/')
file = pd.read_csv('responsesoflockdown.csv')
app.layout = html.Div([
html.Div([
    html.H1("Showing the dashboard on lockdown response collected from all over the India."),
        html.H2("You can choose from the below options"),html.Hr(),
        dcc.Graph(id='our_graph')
    ],className='nine columns'),
    html.Div([
        
    html.Br(),
    html.Div(id='output_data'),
    html.Br(),

    html.Label(['Choose column:'],style={'font-weight': 'bold', "text-align": "center"}),

    dcc.Dropdown(id='my_dropdown',
        options = [
                    {'label' : 'Uttar Pradesh', 'value' : 'Uttar Pradesh' },
                    {'label' : 'Madhya Pradesh', 'value' : 'Madhya Pradesh' },
                    {'label' : 'Andhra Pradesh', 'value' : 'Andhra Pradesh' },
                    {'label' : 'Assam', 'value' : 'Assam' },
                    {'label' : 'Delhi', 'value' : 'Delhi' },
                    {'label' : 'Karnataka', 'value' : 'Karnataka' },
                    {'label' : 'West Bengal', 'value' : 'West Bengal' },
                    {'label' : 'Telangana', 'value' : 'Telangana' },
                    {'label' : 'Tamil Nadu', 'value' : 'Tamil Nadu' },
                    {'label' : 'Bihar', 'value' : 'Bihar' },
                    {'label' : 'Kerela', 'value' : 'Kerela' },
                    {'label' : 'Jharkhand', 'value' : 'Jharkhand' },
                    {'label' : 'Rajasthan', 'value' : 'Rajasthan' },
                    {'label' : 'Pondicherry', 'value' : 'Pondicherry' },
                    {'label' : 'Maharashtra', 'value' : 'Maharashtra' },
                    {'label' : 'Gujarat', 'value' : 'Gujarat' },
                    {'label' : 'Haryana', 'value' : 'Haryana' },
                    ],
                    optionHeight=35,
                    value = 'Uttar Pradesh',
                    searchable=True,
                    placeholder='Please select...',     
                    clearable=True,
                    style={'width':"100%"},
                ),                                  
                                              
        ],className='three columns'),
    ])

@app.callback(
    Output(component_id='our_graph', component_property='figure'),
    [Input(component_id='my_dropdown', component_property='value')]
)             
def build_graph(column_chosen):
    df=file
    fig =px.pie(df,names=column_chosen)
    return fig

@app.callback(
    Output(component_id='output_data', component_property='children'),
    [Input(component_id='my_dropdown', component_property='search_value')]
)

def build_graph(data_chosen):
    return ('Search value was: " {} "'.format(data_chosen))

@server.route('/')
def home():
    return render_template('home.html')

@server.route('/dashboard')
def dashboard():
    return flask.redirect('/dashboard')

@server.route('/tweets')
def tweets():
    return flask.redirect('/tweets')

if __name__=='__main__':
    server.run(debug = True, port=8080)
