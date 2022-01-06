import dash
import math
from dash import dcc
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
                   dtype={'district': int,'dbn': str,	'name': str,
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
year_values = list(year_lookup.values())


# Functions
def build_banner():
   return html.Div(
      id="banner",
      className="banner",
      children=[
        html.Img(src=dash_app.get_asset_url("cunysps_2021_2linelogo_spsblue_1.png"), ),
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
                                    "NYC OpenData SHSAT Admissions Test Offers by Sending School",
                                    href='https://data.cityofnewyork.us/browse?q=shsat'
                                    ),
                                " for 2015-2021. The data stored counts for the total of students in H.S admissions, students who took the SHSAT, and offers made to ",
                                "attend a specialized high school. Schools recorded 0-5 together as a group statistic. So if a middle school had 0 SHSAT offers, it would be recorded as 0-5.",
                            ],
                         ),
                         html.P(
                            children=[
                              "Explore the data. The map will enable you to see the data for the schools and what was recorded.",
                              "Select the year from the dropdown menu to see the statistics for that year.",
                              "When you click on a marker on the map, the bottom bar will be populated with information about the school.",
                              "May you have future success in finding a school for your child!",
                            ]
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
                         html.Br(),

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
                                 dcc.Graph(id='map-graph')
                              ]

                            )
                          )
                     ]
                  ),
               ]
            ),
                html.Div(
      id="bottom-row",
      children=[
          html.Div(
              className="bottom-row",
              id="bottom-row-header",
              children=[
                  html.Div(
                     className="bottom-left-column",
                     id="form-bar-container",
                     children=[
                         build_graph_title("2016-2021 Information"),
                         dcc.Graph(id='form-bar-graph'),
                         html.Br(),
                     ]
                  ),
                  html.Div(
                     className="bottom-right-column",
                     id="form-text-container",
                     children=[
                         html.P(
                            id="lower-text-box"
                            ),
                     ],
                  ),
              ]
              )
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
    	hover_data=['district', 'address', 'telephone', 'dbn', offers_count, 'url'],
    	)

    fig.update_layout(mapbox_style="carto-positron",
    	height=600,
        margin={"r": 30, "t": 57, "l": 30, "b": 23},
        hoverlabel_font_size=11,
        legend_font_size=10,
    	)


    return fig



# Update Text Box
@dash_app.callback(
    Output("lower-text-box", "children"),
    [
        Input("map-graph", "clickData")
    ],
)
def update_textbox(click_data):
    if click_data == None:
        children = [
            build_graph_title("School Information"),
            html.P('Click on a point on the map to display school information'),
        ]
    else:
        name = click_data['points'][0]['hovertext']
        dbn = click_data['points'][0]['customdata'][3]
        district = click_data['points'][0]['customdata'][0]
        address = click_data['points'][0]['customdata'][1]
        telephone = click_data['points'][0]['customdata'][2]
        url = click_data['points'][0]['customdata'][5]
        if (click_data['points'][0]['customdata'][4] > 0):
            offers = click_data['points'][0]['customdata'][4]
        else:
            offers = '0 to 5'
        children = [
          build_graph_title("School Information"),
          html.P(
            children = [
                'School Name: ', 
                html.A('{}'.format(name), href=url),
            ]



            ),
          html.P('DBN: {}'.format(dbn)),
          html.P('District: {}'.format(district)),
          html.P('Address: {}'.format(address)),
          html.P('Telephone: {}'.format(telephone)),
          html.P('Offers: {}'.format(offers)),
          ]

    return children




# Update Bar plot
@dash_app.callback(
    Output("form-bar-graph", "figure"),
    [
        Input("map-graph", "clickData")
    ],
)
def update_bar(click_data):
    if click_data == None:
        dbn = '01M184'
        name = 'P.S. 184m Shuang Wen'
    else:
        dbn = click_data['points'][0]['customdata'][3]
        name = click_data['points'][0]['hovertext']

    testers_count_select = []
    offers_count_select = []

    for i in year_lookup.values():
        testers_count_select.append(str(i) + '_testers_count')
        offers_count_select.append(str(i) + '_offers_count')

    mask = df["dbn"] == dbn
    select = df[mask]
    testers = select[testers_count_select].values.tolist()
    offers = select[offers_count_select].values.tolist()

    temp = [item for sublist in testers for item in sublist]
    testers = temp

    temp = [item for sublist in offers for item in sublist]
    offers = temp

    testers = [2 if x==0 else x for x in testers]
    testers = [0 if math.isnan(x) else x for x in testers]

    offers = [2 if x==0 else x for x in offers]
    offers = [0 if math.isnan(x) else x for x in offers]

    temp_df = pd.DataFrame(list(zip(year_values, testers, offers)),
              columns =['Year', 'Total Testers', 'Number of Offers'])

    temp_df = pd.melt(temp_df, id_vars =['Year'], value_vars =['Total Testers', 'Number of Offers'])



    fig = px.bar(
        temp_df,
        x="Year",
        y="value",
        color="variable",
        barmode="overlay",
        opacity=1,
        labels={
        'value': 'Count',
        'variable': 'Legend',
        },
        title='Historical Information for ' + name,
    )

    fig.update_layout(
        font_size=9,
    )


    return fig




# Running the server
if __name__ == "__main__":
    dash_app.run_server(debug=True)