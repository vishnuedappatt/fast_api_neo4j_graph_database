from py2neo import Graph


def graph():    
    graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))
    graph.run("UNWIND range(1, 3) AS n RETURN n, n * n as n_sq")