from neo4j import GraphDatabase
import neo4j
import pyvis


class Neo4jDriver:

    def __init__(self, uri="bolt://localhost:7687", user="root", password="test_root"):
        """
        Start Neo4j
        Before first use, create admin user "root" and set password to "test_root"
        Change uri if different
        """
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.create_unique_name_constraint()

    def execute_command(self, command, db="academicworld", result_transformer=neo4j.Result.to_eager_result, *args, **kwargs):
        """

        :param command:
        :param db:
        :param result_transformer:
            to dataframe: neo4j.Result.to_df
            to graph: neo4j.Result.graph
        :param args:
        :param kwargs: arguments used in the query
        :return:
        """
        return self.driver.execute_query(command, database_=db, result_transformer_=result_transformer, *args, **kwargs)

    def get_co_author_graph(self, start):
        command = """MATCH (start:FACULTY {name:'%s'}),
        (fav:fav_faculty),
        p = shortestPath((start)-[pub:PUBLISH*]-(f:FACULTY))
        WHERE f.name = fav.name
        AND start.name <> f.name
        RETURN p
        LIMIT 5""" % start
        graph_result = self.execute_command(command, result_transformer=neo4j.Result.graph)
        # print(graph_result.nodes)
        nodes_text_properties = {  # what property to use as text for each node
            "FACULTY": "name",
            "PUBLICATION": "title"
        }
        return visualize_result(graph_result, nodes_text_properties, start)

    def get_all_fav_faculty(self, to_list=False):
        command = "MATCH (n:fav_faculty) RETURN n.name"
        if to_list:
            return [record["n.name"] for record in self.execute_command(command)[0]]
        else:
            return self.execute_command(command, result_transformer=neo4j.Result.to_df)

    def get_all_faculty(self):
        command = "MATCH (n:FACULTY) RETURN n.name"
        return [record["n.name"] for record in self.execute_command(command)[0]]

    def add_fav_faculty(self, name, label='fav_faculty'):
        command = "CREATE (n:%s {name: '%s'})" % (label, name)
        try:
            self.execute_command(command)
        except:
            pass

    def delete_fav_faculty(self, name, label='fav_faculty'):
        command = "MATCH (n:%s {name: '%s'}) DELETE n" % (label, name)
        try:
            self.execute_command(command)
        except:
            pass

    def create_unique_name_constraint(self, label="fav_faculty"):
        command = """
            CREATE CONSTRAINT unique_name IF NOT EXISTS 
            FOR (n:%s)
            REQUIRE n.name IS UNIQUE
        """ % label
        self.execute_command(command)

    def close(self):
        self.driver.close()


def visualize_result(query_graph, nodes_text_properties, start):
    """

    :param start:
    :param query_graph:
    :param nodes_text_properties: dictionary indicating what property to use as text for each node
    :return:
    """
    visual_graph = pyvis.network.Network()
    start_node_id = start_node_text = None
    for node in query_graph.nodes:
        node_label = list(node.labels)[0]
        node_text = node[nodes_text_properties[node_label]]
        if node_text == start:
            start_node_id = node.element_id
            start_node_text = node[nodes_text_properties[node_label]]
        else:
            visual_graph.add_node(node.element_id, node_text, group=node_label)
    visual_graph.add_node(start_node_id, start_node_text, group="start")

    for relationship in query_graph.relationships:
        visual_graph.add_edge(
            relationship.start_node.element_id,
            relationship.end_node.element_id,
            title=relationship.type
        )

    visual_graph.write_html('network.html')
    return visual_graph

