"""
Welsh-Powell greedy graph coloring algorithm.
Sorts vertices by degree in descending order and assigns lowest valid color.
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


def welsh_powell(graph):
    """
    Welsh-Powell graph coloring using greedy heuristic.

    Algorithm:
    1. Sort vertices by degree (descending)
    2. For each vertex, assign the smallest color not used by neighbors

    Args:
        graph: NetworkX graph

    Returns:
        dict: Mapping of vertex -> color
    """
    # Sort vertices by degree in descending order
    vertices = sorted(graph.nodes(), key=lambda v: graph.degree(v), reverse=True)

    color_map = {}

    for vertex in vertices:
        color = get_next_color(graph, vertex, color_map)
        color_map[vertex] = color

    return color_map


def run(graph):
    """
    Run Welsh-Powell algorithm and measure performance.

    Args:
        graph: NetworkX graph

    Returns:
        tuple: (color_map dict, num_colors used, runtime_ms float)
    """
    start = time.perf_counter()
    color_map = welsh_powell(graph)
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
