from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import pprint
import neo4j
import random
from neo4j_utils import Neo4jDriver, visualize_result
from mysql_utils import SQLDriver
from mongodb_utils import MongoDriver
from dash_utils import *

app = Dash(__name__)

# query mySQL
sql = SQLDriver()
popular_keywords = sql.get_popular_keywords()
# print(popular_keywords[:10])
keyword = 'machine learning'    # TODO: need to get from dropdown menu, available options are popular_keywords
year_lower = 2010   # TODO: need to get from range slider
year_upper = 2012   # TODO: need to get from range slider
publication_df = sql.get_top_n_publications(keyword, year_lower, year_upper, 5)
# print(publication_df.head())
# TODO: display publication_df in a table in first widget

faculty_df = sql.get_top_n_faculties(5)
# print(faculty_df.head())
# TODO: display faculty_df in a table in third widget
university_df = sql.get_top_n_universities(5)
# print(university_df)
# TODO: display university_df in a table in second widget

# query mongodb
mongo = MongoDriver()
faculty_name = "Craig Zilles"   # TODO: need to get from dropdown menu, available options are from faculty_df
faculty_info = mongo.get_faculty(faculty_name)
# pprint.pprint(faculty_info)
# TODO: display faculty_info and photo in fourth widget

# query neo4j and display result network on dash
graphdb = Neo4jDriver()
faculty_names = faculty_df['name'].values.tolist()
for name in faculty_names:
    graphdb.add_fav_faculty(name)   # TODO: need user manually add fav_faculty from dropdown menu

app.layout = html.Div(children=[create_widget_five(graphdb), create_widget_six(graphdb)])

graphdb.close()
mongo.close()


if __name__ == '__main__':
    # change to debug=False if cannot load page
    app.run(debug=True)
