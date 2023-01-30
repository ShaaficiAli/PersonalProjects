from dash import Dash,html, dcc,Input,Output
import plotly.express as px
import pandas as pd
import re
import json
import sqlite3
import tft_utils
app = Dash(__name__)
conn = sqlite3.connect('Data/league_match.db')
unitdataframe = pd.read_sql_query('select * from units JOIN placements on units.placement_id == placements.placement_id',conn)
unitUniqueName = unitdataframe['unitname'].unique()
unitAvgPlacementRate = unitdataframe.groupby('unitname')['placement'].mean()
unitWin = unitdataframe.apply(lambda x:1 if x['placement']<=4 else 0,axis=1)
unitdataframe['is_win'] = unitWin
unitTotalWins = unitdataframe.groupby('unitname')['is_win'].sum()
unitTotalCount = unitdataframe['unitname'].value_counts()
unitTotals = pd.concat([unitTotalWins,unitTotalCount],axis=1).reset_index().rename(columns={'unitname':'totalCount','index':'unitname'})
unitTotals['winrate'] = unitTotals['is_win']/unitTotals['totalCount']
'''
app.layout = html.Div([
    html.title("average placements per unit selected"),
    html.Div([
        "unit selected: ",
        dcc.Dropdown(unitUniqueName,'TFT8_Blitzcrank',id='unit-dropdown'),
        dcc.Output()])
           
    ])
@app.callback(
    Output(''),
    Input())
def update_unitPlacementAvg(unit):
      avg = unitAvgWinrate
      count_matches = 

@app.callback(
    Output(),
    Input('unit-dropdown','unit')
)
def update_unitGraph(unit):
    pass

@app.callback(
    Output(),
    Input())
def update_unitVSGraph(unit1,unit2):
    pass
'''
