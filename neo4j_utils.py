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
        self.uri = uri
        self.user = user
        self.password = password

    def query(self, query_str, db="academicworld", result_transformer=neo4j.Result.to_df, *args, **kwargs):
        """

        :param query_str:
        :param db:
        :param result_transformer:
            to dataframe: neo4j.Result.to_df
            to graph: neo4j.Result.graph
        :param args:
        :param kwargs: arguments used in the query
        :return:
        """
        with GraphDatabase.driver(self.uri, auth=(self.user, self.password)) as driver:
            return driver.execute_query(query_str, database_=db, result_transformer_=result_transformer, *args,
                                        **kwargs)


def visualize_result(query_graph, nodes_text_properties):
    """

    :param query_graph:
    :param nodes_text_properties: dictionary indicating what property to use as text for each node
    :return:
    """
    visual_graph = pyvis.network.Network()

    for node in query_graph.nodes:
        node_label = list(node.labels)[0]
        node_text = node[nodes_text_properties[node_label]]
        visual_graph.add_node(node.element_id, node_text, group=node_label)

    for relationship in query_graph.relationships:
        visual_graph.add_edge(
            relationship.start_node.element_id,
            relationship.end_node.element_id,
            title=relationship.type
        )

    visual_graph.write_html('network.html')
    return visual_graph


if __name__ == "__main__":
    pass
    # Examples:
    # graphdb = Neo4jDriver()
    # query1 = """
    # MATCH (f1:FACULTY)-[p1:PUBLISH]->(pub:PUBLICATION)<-[p2:PUBLISH]-(f2:FACULTY),
    # (f1:FACULTY)-[a1:AFFILIATION_WITH]->(u1:INSTITUTE {name: $university_name}),
    # (f2:FACULTY)-[a2:AFFILIATION_WITH]->(u2:INSTITUTE)
    # WHERE u2.name <> $university_name
    # RETURN u2.name AS University, COUNT(DISTINCT f1) AS count
    # ORDER BY count DESC
    # LIMIT 10
    # """
    # db_result = graphdb.query(query1, university_name="University of illinois at Urbana Champaign")
    # print(db_result)
    #
    # query2 = """MATCH (CZ:FACULTY {name:$faculty_name}),
    # (f:FACULTY)-[:AFFILIATION_WITH]->(i:INSTITUTE {name: $university_name}),
    # p = shortestPath((CZ)-[:INTERESTED_IN*]-(f))
    # RETURN p
    # LIMIT 5"""
    # graph_result = graphdb.query(query2, result_transformer=neo4j.Result.graph,
    #                              faculty_name="Craig Zilles",
    #                              university_name="Carnegie Mellon University")
    # nodes_text_properties = {
    #     "FACULTY": "name",
    #     "KEYWORD": "name"
    # }
    # visualize_result(graph_result, nodes_text_properties)
    # graphdb.close()
    #
