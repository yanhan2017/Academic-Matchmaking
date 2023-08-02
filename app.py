from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import pprint
import neo4j
from neo4j_utils import Neo4jDriver, visualize_result
from mysql_utils import SQLDriver
from mongodb_utils import MongoDriver

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
query2 = """MATCH (CZ:FACULTY {name:$faculty_name}),
    (f:FACULTY)-[:AFFILIATION_WITH]->(i:INSTITUTE {name: $university_name}),
    p = shortestPath((CZ)-[:INTERESTED_IN*]-(f))
    RETURN p
    LIMIT 5"""
graph_result = graphdb.execute_command(query2, result_transformer=neo4j.Result.graph,
                                       faculty_name=faculty_name,
                                       university_name="Carnegie Mellon University")
nodes_text_properties = {  # what property to use as text for each node
    "FACULTY": "name",
    "KEYWORD": "name"
}
visual_graph = visualize_result(graph_result, nodes_text_properties)

app.layout = html.Div(children=[
    html.Iframe(srcDoc=visual_graph.html,
                style={"height": "1067px", "width": "100%"})
])
graphdb.close()
mongo.close()

# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

# app.layout = html.Div([
#     html.H1(children='Title of Dash App', style={'textAlign':'center'}),
#     dcc.Dropdown(df.country.unique(), 'Canada', id='dropdown-selection'),
#     dcc.Graph(id='graph-content')
# ])

# @callback(
#     Output('graph-content', 'figure'),
#     Input('dropdown-selection', 'value')
# )
# def update_graph(value):
#     dff = df[df.country==value]
#     return px.line(dff, x='year', y='pop')

if __name__ == '__main__':
    # change to debug=False if cannot load page
    app.run(debug=True)
