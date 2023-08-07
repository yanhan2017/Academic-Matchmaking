from dash import Dash, html, dcc, callback, Output, Input, State, dash_table, ctx
import plotly.express as px
from neo4j_utils import Neo4jDriver
from mysql_utils import SQLDriver
from mongodb_utils import MongoDriver
from PIL import Image
import requests
from dash_utils import *

app = Dash(__name__)

colors = {
    'background': '#111111',
    'text': '#d3d3d3',
    "header": '#BFC9CA'
}

# query mySQL
sql = SQLDriver()
popular_keywords = sql.get_popular_keywords()
keyword = 'machine learning'    # TODO: need to get from dropdown menu, available options are popular_keywords
year_lower = 2010   # TODO: need to get from range slider
year_upper = 2012   # TODO: need to get from range slider
publication_df = sql.get_top_n_publications(keyword, year_lower, year_upper, 5)

faculty_df = sql.get_top_n_faculties(5)
university_df = sql.get_top_n_universities(5)

# query mongodb
mongo = MongoDriver()
faculty_name = "Craig Zilles"   # TODO: need to get from dropdown menu, available options are from faculty_df
faculty_info = mongo.get_faculty(faculty_name)

# Get Faculty Image
url = faculty_info['photoUrl']
try:
    img = Image.open(requests.get(url, stream=True).raw)
    fig = px.imshow(img)
    fig.update_layout(coloraxis_showscale=False)
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)
except Exception as e:
    img = Image.open(requests.get('http://www.srobertsonpottery.com/images/catalogue/nophoto.jpg', stream=True).raw)
    fig = px.imshow(img)
    fig.update_layout(coloraxis_showscale=False)
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)

# query neo4j and display result network on dash
graphdb = Neo4jDriver()
app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    # Main Header of the Web
    html.Br(),
    html.Div([html.H1('Academic Matchmaking: Find Your Academic Advisor', style={'textAlign': 'center', 'color': colors['header'], 'font-size': 40})]),
    html.Br(),

    # Widget 0 - Dropdown Menu for Users to Choose Keywords + Year Range Slider
    html.Div(children=[
        # Dropdown Menu
        html.Div([
            html.Label('Choose Your Keyword ', style={'textAlign': 'center', 'color': colors['text']}),
            html.Br(),
            dcc.Dropdown(popular_keywords, value=popular_keywords[0], style={'color': 'black'},
                         id='kw_dropdown')
            ], style={'padding': 15, 'flex': 1, 'font-size': 20}),

        # Year & Range
        html.Div([
            html.Label('Choose Your Interested Year Range ', style={'textAlign': 'center', 'color': colors['text']}),
            html.Br(),
            dcc.RangeSlider(1903, 2021, 1, marks=None,
                            value=[1978, 2000], tooltip={"placement": "bottom", "always_visible": True},
                            id='year_slider')
            ], style={'padding': 15, 'flex': 1, 'font-size': 20}),

        # Button to Explore & Refresh Results
        html.Div([
            html.Label('See Your Top publications, Universities, and Faculties', style={'textAlign': 'center', 'color': colors['text']}),
            html.Br(),
            html.Button('Explore!', id='submit_choices', n_clicks=0, style={'height': '50px', 'width': '100px'})
            ], style={'padding': 15, 'flex': 1, 'font-size': 20}),

    ], style={'display': 'flex', 'flex-direction': 'row'}),

    html.Br(),

    # Widgets 1 & 2 - Top Publications and Universitiesfor the Users' Inputs in Widget 0
    html.Div(children=[
        # Widget 1 - Top Publications Title,
        html.Div([html.Label('Top Publications', style={'textAlign': 'center', 'color': colors['text'], 'padding': 15}),
          html.Br(),
        dash_table.DataTable(data=publication_df.to_dict('records'), id='top_pub',
                             style_as_list_view=True, style_cell={'padding': '25px', 'width': '600px', 'overflow': 'auto', 'font-size': 13},
                             style_header={
                                'backgroundColor': 'white',
                                'fontWeight': 'bold'},
                             style_table={'width': '10%', 'padding': 10, 'flex': 1},
                             )], style={"flex": '0 0 60%'}),

        # Widget 2 - Top Universities Info
        html.Div([html.Label('Top Universities', style={'textAlign': 'center', 'color': colors['text'], 'padding': 15}),
                  html.Br(),
        dash_table.DataTable(data=university_df.to_dict('records'), id='top_uni',
                             style_as_list_view=True, style_cell={'padding': '25px', 'width': '600px', 'overflow': 'auto', 'font-size': 16},
                             style_header={
                                'backgroundColor': 'white',
                                'fontWeight': 'bold'},
                             style_table={'width': '10%', 'padding': 10, 'flex': 1},
                             )], style={"flex": '0 0 40%'}),

    ], style={'display': 'flex', 'flex-direction': 'row', 'font-size': 20}),

    html.Br(),

    # Widget 3 & 4 - Top Faculties and Their Info from Users' Inputs in Widget 0
    html.Div(children=[
        # Widget 3 - Top Faculties Info
        html.Div([html.Label('Top Faculties', style={'textAlign': 'center', 'color': colors['text'], 'padding': 15}),
            html.Br(),
            dash_table.DataTable(data=faculty_df.to_dict('records'), id='top_fac',
                                 style_as_list_view=True, style_cell={'padding': '25px', 'width': '600px', 'overflow': 'auto'},
                                 style_header={
                                     'backgroundColor': 'white',
                                     'fontWeight': 'bold'},
                                 style_table={'width': '95%', 'padding': 15, 'flex': 1}
                                 )], style={"flex": '0 0 60%'}),

        # Widget 4 - Choosing Users' Favorite Professor from Widget 3 to See Their Info
        # Dropdown Menu to Choose Professors from Widget
        html.Div(
            [html.Div(children=[
                    html.Label('Choose Your Top Professor', style={'textAlign': 'center', 'color': colors['text']}),
                    dcc.Dropdown(options=faculty_df['Name'], value=faculty_df['Name'].iat[0], style={'color': 'black'},
                                 id='fac_dropdown'),
                ], style={'width': '75%', 'padding': 15}),

            # Faculty Info of User-Chosen Faculty
            html.Div(children=[
                html.Label('Name: %s' % faculty_info['name'], id='fac_name', style={'textAlign': 'center', 'color': colors['text']}),
                html.Br(),
                html.Label('University: %s' % faculty_info['affiliation']['name'], id='uni_name', style={'textAlign': 'center', 'color': colors['text']}),
                html.Br(),
                html.Label('Position: %s' % faculty_info['position'], id='fac_pos', style={'textAlign': 'center', 'color': colors['text']}),
                html.Br(),
                dcc.Graph(figure=fig, id='fac_img',
                          style={'height': '450px', 'width': '450px'}
                          )
            ], style={'width': '75%', 'padding': 15})], style={"flex": '0 0 40%'}),

    ], style={'display': 'flex', 'flex-direction': 'row', 'font-size': 20}),

    html.Br(),

    # Widget 5 & 6 -
    html.Div(children=[
        create_widget_five(graphdb),
        create_widget_six(graphdb)

    ], style={'display': 'flex', 'flex-direction': 'row', 'font-size': 20})

])


@callback(
    Output(component_id='top_pub', component_property='data'),
    Output(component_id='top_uni', component_property='data'),
    Output(component_id='top_fac', component_property='data'),
    Input(component_id='submit_choices', component_property='n_clicks'),
    [State(component_id='kw_dropdown', component_property='value'),
    State(component_id='year_slider', component_property='value')],
    prevent_initial_call=True
)
def update_kw_output(n_clicks, kw_dropdown, year_slider):
    if n_clicks > 0:
        publication_df = sql.get_top_n_publications(kw_dropdown, year_slider[0], year_slider[1], 5)
        university_df = sql.get_top_n_universities(5)
        faculty_df = sql.get_top_n_faculties(5)
        return publication_df.to_dict('records'), university_df.to_dict('records'), faculty_df.to_dict('records')


@callback(
    Output(component_id='fac_dropdown', component_property='options'),
    [Input(component_id='top_fac', component_property='data')],
    prevent_initial_call=True
)
def update_fac_dropdown(top_fac):
    return [d['Name'] for d in top_fac]

@callback(
    Output(component_id='fac_name', component_property='children'),
    Output(component_id='uni_name', component_property='children'),
    Output(component_id='fac_pos', component_property='children'),
    Output(component_id='fac_img', component_property='figure'),
    [Input(component_id='fac_dropdown', component_property='value')],
    prevent_initial_call=True
)
def update_fav_fac(value):
    faculty_info = mongo.get_faculty(value)
    url = faculty_info['photoUrl']
    try:
        img = Image.open(requests.get(url, stream=True).raw)
        fig = px.imshow(img)
        fig.update_layout(coloraxis_showscale=False)
        fig.update_xaxes(showticklabels=False)
        fig.update_yaxes(showticklabels=False)
    except Exception as e:
        img = Image.open(requests.get('http://www.srobertsonpottery.com/images/catalogue/nophoto.jpg', stream=True).raw)
        fig=px.imshow(img)
        fig.update_layout(coloraxis_showscale=False)
        fig.update_xaxes(showticklabels=False)
        fig.update_yaxes(showticklabels=False)

    return 'Name: %s' % faculty_info['name'], 'University: %s' % faculty_info['affiliation']['name'], \
        'Position: %s' % faculty_info['position'], fig


if __name__ == '__main__':
    # change to debug=False if cannot load page
    app.run(debug=False)
    graphdb.close()
    mongo.close()

