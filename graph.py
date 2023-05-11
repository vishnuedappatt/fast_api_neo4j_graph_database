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


def create_person_node(label: str, propreties):
    return Node(
        label,
        name=propreties.name,
        password=propreties.password,
        username=propreties.username,
    )


def matching_person_node(g):
    # n_matching=
    return NodeMatcher(g)
