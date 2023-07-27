from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
from neo4j_utils import Neo4jDriver, visualize_result
from mysql_utils import SQLDriver
from mongodb_utils import MongoDriver

app = Dash(__name__)

# query mySQL
sql = SQLDriver()
query1 = ("SELECT * FROM faculty "
          "LIMIT %s")
limit = 10
df = sql.query_to_df(query1, [limit])
# print(df.head())

# query mongodb
faculty_name = "Craig Zilles"
mongo = MongoDriver()
sample1 = mongo.db.faculty.find_one({"name": faculty_name})
pprint.pprint(sample1['keywords'])

year = 2012
pipeline = [
    {"$match": {"year": {"$gte": year}}},
    {"$unwind": "$keywords"},
    {"$group": {
        "_id": "$keywords.name",
        "publicationCount": {
            "$sum": 1
        }
    }
    },
    {"$sort": {"publicationCount": -1}},
    {"$limit": 10}
]

result = mongo.db.publications.aggregate(pipeline)
pprint.pprint(list(result))

# query neo4j and display result network on dash
graphdb = Neo4jDriver()
query2 = """MATCH (CZ:FACULTY {name:$faculty_name}),
    (f:FACULTY)-[:AFFILIATION_WITH]->(i:INSTITUTE {name: $university_name}),
    p = shortestPath((CZ)-[:INTERESTED_IN*]-(f))
    RETURN p
    LIMIT 5"""
graph_result = graphdb.query(query2, result_transformer=neo4j.Result.graph,
                             faculty_name="Craig Zilles",
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
    app.run(debug=True)
