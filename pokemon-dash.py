# Imports
import dash
from dash import html, dcc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import pymssql
from dash.dependencies import Input, Output
import numpy as np

# Get configuration info
from config import database, user, password, table, server

# Initialize app
app = dash.Dash(__name__)

# Create function for getting table info
def getPokemonTable():
    conn = pymssql.connect(server,user,password,database)
    cursor = conn.cursor()
    query = f"SELECT * FROM {table}"
    df = pd.read_sql(query,conn)
    return df

def createPokemonCtBarGraph():

    # Get Pokemon table
    df = getPokemonTable()

    # Refine what data the bar graph needs
    df = df.groupby('name')['name'].count()
    pokemon = df.index.to_list()
    cts = df.to_list()
    df = pd.DataFrame({'name': pokemon, 'ct': cts})
    df = df.sort_values('ct')
    df = df.head(n=25)
    df['name'] = df['name'].str.capitalize()

    # Plot on bar graph
    fig = px.bar(df, x='name', y='ct', title='Top 25 Most Common Pokémon',
        labels={'name': 'Pokémon', 'ct': 'Number of Instances'})
    return fig

def createPrimaryTypeCtBarGraph():

    # Get Pokemon table
    df = getPokemonTable()

    # Refine what data the bar graph needs
    df = df.groupby('primary_type')['primary_type'].count()
    types = df.index.to_list()
    cts = df.to_list()
    df = pd.DataFrame({'primary_type': types, 'ct': cts})
    df = df.sort_values('ct')
    df['primary_type'] = df['primary_type'].str.capitalize()

    # Plot on bar graph
    fig = px.bar(df, x='primary_type', y='ct', title='Most Common Primary Types of Pokemon',
        labels={'primary_type': 'Primary Type', 'ct': 'Number of Instances'})
    return fig

def createSecondaryTypeCtBarGraph():

    # Get Pokemon table
    df = getPokemonTable()

    # Refine what data the bar graph needs
    df = df.groupby('secondary_type')['secondary_type'].count()
    types = df.index.to_list()
    cts = df.to_list()
    df = pd.DataFrame({'secondary_type': types, 'ct': cts})
    df = df.sort_values('ct')
    df['secondary_type'] = df['secondary_type'].str.capitalize()
    df = df.loc[df['secondary_type'] != 'N/a']

    # Plot on bar graph
    fig = px.bar(df, x='secondary_type', y='ct', title='Most Common Secondary Types of Pokemon',
        labels={'secondary_type': 'Secondary Type', 'ct': 'Number of Instances'})
    return fig

def getPokemonCt():

    # Get Pokemon table
    df = getPokemonTable()

    # Refine what data the bar graph needs
    ct = df.shape[0]

    return f'There are {ct} Pokémon now in the database!'

def getPokemonLoc():

    # Get Pokemon table
    df = getPokemonTable()

    # Refine what data the bar graph needs
    df = df.groupby(['lat', 'long'])[['lat', 'long']].count()
    coords = df.index.to_list()
    lats = []
    longs = []
    for coord in coords:
        lats.append(coord[0])
        longs.append(coord[1])
    cts = df['lat'].to_list()
    df = pd.DataFrame({'lat': lats, 'lon': longs, 'ct': cts})

    # Create fig
    fig = px.scatter_geo(df, lat='lat', lon='lon',
                     size='ct', title='Locations of Pokemon')
    
    # Return figure
    return fig
    

getPokemonLoc()

app.layout = html.Div(children=[
    html.H1(children='Hello World!'),

    html.H3(children=getPokemonCt()),

    dcc.Graph(
        id='MostFreqPokemon',
        figure=createPokemonCtBarGraph()
    ),

    dcc.Graph(
        id='MostFreqPrimaryType',
        figure=createPrimaryTypeCtBarGraph()
    ),

    dcc.Graph(
        id='MostFreqSecondaryType',
        figure=createSecondaryTypeCtBarGraph()
    ),

    dcc.Graph(
        id='PokemonLocations',
        figure=getPokemonLoc()
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)