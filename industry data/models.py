import pandas as pd
from dash import Dash, html, dcc
import plotly.express as px
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
metrics = pd.read_csv("metrics.csv",encoding='cp1252')
unemployement = pd.read_csv("Unemployment_-_1410002301-eng_6.csv")
sector = pd.read_csv("Sector_-_cews_tbl2_4_1.csv")

#cws = pd.read_csv("")

