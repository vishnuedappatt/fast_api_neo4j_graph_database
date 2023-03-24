from py2neo import Graph, Node, NodeMatcher, RelationshipMatcher


def init_graph():
    graph = Graph("bolt://localhost:7687", auth=("neo4j", "fastapi1"))
    return graph


def create_node(label: str, propreties):
    return Node(label, name=propreties.name, password=propreties.password)


# def node_macher():
#     return NodeMatcher()


# def  relationship_matcher():
#     return RelationshipMatcher()
