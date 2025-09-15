import pandas as pd
import numpy as np
from dash import Dash, html, dcc,Input,Output,State,dash_table
import plotly.express as px
from os import listdir
from os.path import isfile, join
from functools import reduce
import re
datasets = [f for f in listdir(".") if isfile(join(".", f)) and "csv" in f]

def data_prep_WorldData_csv(filename):
    metric_name = re.sub(".csv","",filename)
    df = pd.read_csv(filename,skiprows=4)
    df = df.filter(regex="Country Name|(\d\d\d\d)")
    df = df.loc[:,df.columns!="2022"]
    df = df.melt(id_vars ="Country Name",
                 var_name = "year",
                 value_name = metric_name)
    
    return df
dataframes = [data_prep_WorldData_csv(dataset) for dataset in datasets]
CountryData = alls = reduce(lambda  left,right: pd.merge(left,right,on=['Country Name','year'],
                                            how='inner'), dataframes)
Features = CountryData.columns.values.tolist()
CountryNames = CountryData['Country Name'].unique()

CountryDataPPfig = px.line(CountryData,x="year",y=Features[5])

app=Dash(__name__)

CountryDataPPDiv = html.Div([
    html.H1("Country Data for various features"),
    dcc.Dropdown(Features[2:],Features[2],id='Feature_Dropdown'),
    dcc.Dropdown(CountryNames,value = [CountryNames[0]],multi=True,id='Country_Dropdown'),
    html.Button('Submit', id='submit-country', n_clicks=0),
    dcc.Graph(figure = CountryDataPPfig,id='Country-Data-figure')
    ])
@app.callback(
    Output('Country-Data-figure','figure'),
    Input('submit-country','n_clicks'),
    State('Feature_Dropdown','value'),
    State('Country_Dropdown','value')
    
)
def update_select_country(n_clicks,feature,countries):
    data = CountryData[CountryData['Country Name'].isin(countries)]
    figure = px.line(data,x = 'year',y=feature,color='Country Name')
    return figure
   
app.layout =html.Div([CountryDataPPDiv])
if __name__ == '__main__':
    app.run_server(debug=True,port=6969)

