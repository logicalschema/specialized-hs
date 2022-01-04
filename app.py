import json
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px

# external JavaScript files
#external_scripts = [
#    {
#        'src': 'https://www.googletagmanager.com/gtag/js?id=G-ET46TBPVET',
#    }
#]



# app initialize
dash_app = dash.Dash(
    __name__,
    external_scripts=external_scripts,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],

)


app = dash_app.server
dash_app.config["suppress_callback_exceptions"] = True
dash_app.title = 'NYC Specialized High School Offers By Middle School: 2016-2021'
dash_app._favicon = ('assets/favicon.ico')


# Load data
df = pd.read_csv("complete.csv",
                   dtype={'district': int,'schooldbn': str,	'name': str,
                   'telephone': str, 'address': str, 'Postcode': str,
                   'Borough': str, 'url': str, 'Latitude': float, 'Longitude': float,
                   })


# Setup variables
center = {"lat": 40.70229736498986, "lon": -74.01581689028704}
colormap = {
  '0-5': '#e41a1c',
  '6-50': '#377eb8',
  '51-100': '#4daf4a',
  '101-200': '#984ea3',
  '201+': '#ff7f00',
}



# Functions
def build_banner():
   return html.Div(
      id="banner",
      className="banner",
      children=[
        html.Img(src=dash_app.get_asset_url("cunysps_2021_2linelogo_spsblue_1.png"), style={'height':'75%', 'width':'75%'}),
        html.H6("NYC Specialized High School Offers By Middle School: 2016-2021"),
        ],
    )


def build_graph_title(title):
   return html.P(className="graph-title", children=title)


