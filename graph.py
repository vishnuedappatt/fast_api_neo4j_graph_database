import os

from dotenv import load_dotenv
from py2neo import Graph, Node, NodeMatcher, RelationshipMatcher

load_dotenv()
host = os.getenv("NEO4J_HOST")
password = os.getenv("NEO4J_PASSWORD")
user = os.getenv("NEO4J_USER")


def init_graph():
    graph = Graph(host, auth=(user, password))
    return graph


def create_node(label: str, propreties):
    return Node(label, name=propreties.name, password=propreties.password)


# def node_macher():
#     return NodeMatcher()


# def  relationship_matcher():
#     return RelationshipMatcher()
