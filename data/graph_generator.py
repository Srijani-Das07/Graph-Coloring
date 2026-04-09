import networkx as nx
import random

def generate_random_graph(n, p, seed=42):
    """Erdos-Renyi random graph. n = vertices, p = edge probability."""
    return nx.erdos_renyi_graph(n, p, seed=seed)

def generate_cycle_graph(n):
    return nx.cycle_graph(n)

def generate_complete_graph(n):
    return nx.complete_graph(n)

def generate_bipartite_graph(n1, n2, p, seed=42):
    return nx.bipartite.random_graph(n1, n2, p, seed=seed)

if __name__ == "__main__":
    G = generate_random_graph(20, 0.4)
    print(f"Vertices: {G.number_of_nodes()}, Edges: {G.number_of_edges()}")
    print("Graph generator working.")
    