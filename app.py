import json
import dash
# import dash_core_components as dcc
from dash import dcc
# import dash_html_components as html
from dash import html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px


# external JavaScript files
external_scripts = [
    {
        'src': 'https://www.googletagmanager.com/gtag/js?id=G-ET46TBPVET',
    }
]



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
dash_app.title = 'NYC Specialized High School Offers By Middle School: 2015-2021'
dash_app._favicon = ('assets/favicon.ico')


# Load data
df = pd.read_csv("assets/complete.csv",
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

years = ['2015-2016', '2016-2017', '2017-2018', '2018-2019', '2019-2020', '2020-2021']
year_lookup = {
	'2015-2016': 2016, 
	'2016-2017': 2017, 
	'2017-2018': 2018, 
	'2018-2019': 2019, 
	'2019-2020': 2020, 
	'2020-2021': 2021,
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



dash_app.layout = html.Div(
  children=[
    html.Div(
        id="top-row",
        children=[
            html.Div(
               className="row",
               id="top-row-header",
               children=[
                  html.Div(
                     className="column",
                     id="header-container",
                     children=[
                         build_banner(),
                         html.P(
                            id="instructions",
                            children=[
                                "This Dash app utilizes data from ",
                                html.A(
                                    "NYC OpenData",
                                    href='https://data.cityofnewyork.us/'
                                    ),
                                ".",
                            ],
                         ),
                         html.Hr(className="divider"),
                         build_graph_title(html.B("Years")),
                         dcc.Dropdown(
                           id="year-dropdown",
                           options=[
                               {"label": i, "value": i} for i in years
                           ],
                           value=years[5],
                           clearable=False
                           ),

                   ]
                  ),
                  html.Div(
                     className="column",
                     id="top-row-graphs",
                     children=[

                          dcc.Loading(
                            html.Div(
                              id="map",
                              className="row",
                              children=[
                              # dcc Graph here
                                 dcc.Graph(id='map-graph')
                              ]

                            )
                          )
                     ]
                  ),
               ]
            ),
          ]
    ),
])







# Update map
@dash_app.callback(
    Output("map-graph", "figure"),
    [
        Input("year-dropdown", "value"),
    ],
)
def update_map(year_dropdown_name):

    year = year_lookup[year_dropdown_name]


    # Selection of specific columns for plotting
    student_count = str(year) + '_student_count'
    testers_count = str(year) + '_testers_count'
    offers_count = str(year) + '_offers_count'


    selection_columns = ['dbn', 'district', 'name', 'telephone', 'address', 'Postcode', 'Borough' , 'url', 'Latitude', 'Longitude', student_count, testers_count, offers_count]
    mapdf = df[selection_columns].copy()

    mapdf = mapdf[mapdf[offers_count].notna()]
    mapdf['Offers'] = pd.cut(x=mapdf[offers_count], bins=[0, 6, 50, 100, 200, 400], labels=['0-5', '6-50', '51-100', '101-200', '201+'], include_lowest=True)


    fig = px.scatter_mapbox(mapdf, 
    	lat='Latitude', 
    	lon='Longitude', 
    	color_discrete_map=colormap,
    	color="Offers",
    	center = center, 
    	zoom=10,
    	hover_name='name',
    	hover_data=['district', 'address', 'telephone', 'dbn', offers_count],
    	)

    fig.update_layout(mapbox_style="carto-positron",
    	width=800,
    	height=800,
    	)

    return fig






# Running the server
if __name__ == "__main__":
    dash_app.run_server(debug=True)