"""
DSATUR (Degree of Saturation) graph coloring algorithm.
Selects vertex with maximum saturation degree and breaks ties by degree.
"""
import time


def get_next_color(graph, vertex, color_map):
    """
    Find the smallest color not used by any neighbor of vertex.

    Args:
        graph: NetworkX graph
        vertex: Target vertex
        color_map: Current color assignment dict

    Returns:
        Smallest valid color (int)
    """
    neighbor_colors = set(
        color_map[n] for n in graph.neighbors(vertex) if n in color_map
    )

    color = 0
    while color in neighbor_colors:
        color += 1
    return color


def get_saturation(graph, vertex, color_map):
    """
    Calculate saturation degree of a vertex.
    Saturation = number of distinct colors in its neighborhood.

    Args:
        graph: NetworkX graph
        vertex: Target vertex
        color_map: Current color assignment dict

    Returns:
        int: Saturation degree
    """
    neighbor_colors = set(
        color_map[n] for n in graph.neighbors(vertex) if n in color_map
    )
    return len(neighbor_colors)


def dsatur(graph):
    """
    DSATUR (Degree of Saturation) greedy coloring algorithm.

    Algorithm:
    1. At each step, select the uncolored vertex with highest saturation
    2. Break ties by selecting vertex with highest degree
    3. Assign the smallest valid color to selected vertex

    Args:
        graph: NetworkX graph

    Returns:
        dict: Mapping of vertex -> color
    """
    color_map = {}
    saturation = {v: 0 for v in graph.nodes()}
    degrees = {v: graph.degree(v) for v in graph.nodes()}

    uncolored = set(graph.nodes())

    while uncolored:
        # Select vertex with max saturation, break ties by degree
        vertex = max(uncolored, key=lambda v: (saturation[v], degrees[v]))

        # Assign the smallest valid color
        color = get_next_color(graph, vertex, color_map)
        color_map[vertex] = color

        # Update saturation of uncolored neighbors
        for neighbor in graph.neighbors(vertex):
            if neighbor in uncolored:
                saturation[neighbor] = get_saturation(graph, neighbor, color_map)

        uncolored.remove(vertex)

    return color_map


def run(graph):
    """
    Run DSATUR algorithm and measure performance.

    Args:
        graph: NetworkX graph

    Returns:
        tuple: (color_map dict, num_colors used, runtime_ms float)
    """
    start = time.perf_counter()
    color_map = dsatur(graph)
    end = time.perf_counter()

    runtime = (end - start) * 1000
    num_colors = len(set(color_map.values()))

    return color_map, num_colors, runtime


if __name__ == "__main__":
    import sys
    sys.path.append(".")
    from data.graph_generator import generate_random_graph

    G = generate_random_graph(20, 0.4)
    color_map, num_colors, runtime = run(G)
    print(f"Colors used: {num_colors}")
    print(f"Runtime: {runtime:.4f} ms")
    print(f"Color map: {color_map}")