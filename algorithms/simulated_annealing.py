import time
import random
import math


def count_conflicts(graph, color_map):
    return sum(1 for u, v in graph.edges()
               if color_map.get(u) == color_map.get(v))


def greedy_initial_coloring(graph):
    """Create initial coloring using greedy approach."""
    color_map = {}
    for vertex in sorted(graph.nodes(), key=lambda v: graph.degree(v), reverse=True):
        neighbor_colors = set(
            color_map[n] for n in graph.neighbors(vertex) if n in color_map
        )
        color = 0
        while color in neighbor_colors:
            color += 1
        color_map[vertex] = color
    return color_map


def simulated_annealing(graph, initial_temp=2.0, cooling_rate=0.999, max_iter=10000):
    """
    Simulated annealing for graph coloring.
    Starts from a random coloring, minimizes conflicts.
    Hard iteration cap prevents unbounded runtime on dense graphs.
    """
    nodes = list(graph.nodes())
    # Use greedy coloring to determine k, then start randomly
    greedy = {}
    for v in sorted(nodes, key=lambda v: graph.degree(v), reverse=True):
        used = {greedy[nb] for nb in graph.neighbors(v) if nb in greedy}
        c = 0
        while c in used:
            c += 1
        greedy[v] = c
    k = len(set(greedy.values()))

    current_coloring = {v: random.randint(0, k - 1) for v in nodes}
    current_conflicts = count_conflicts(graph, current_coloring)
    best_coloring = current_coloring.copy()
    best_conflicts = current_conflicts

    temperature = initial_temp
    iteration = 0

    while temperature > 0.01 and iteration < max_iter:
        vertex = random.choice(nodes)
        old_color = current_coloring[vertex]
        new_color = random.randint(0, k - 1)

        if new_color == old_color:
            temperature *= cooling_rate
            iteration += 1
            continue

        current_coloring[vertex] = new_color
        new_conflicts = count_conflicts(graph, current_coloring)
        delta = new_conflicts - current_conflicts

        if delta < 0 or random.random() < math.exp(-delta / max(temperature, 1e-10)):
            current_conflicts = new_conflicts
            if new_conflicts < best_conflicts:
                best_coloring = current_coloring.copy()
                best_conflicts = new_conflicts
        else:
            current_coloring[vertex] = old_color

        temperature *= cooling_rate
        iteration += 1

    return best_coloring

def run(graph, initial_temp=2.0, cooling_rate=0.999, max_iter=10000):
    """Run simulated annealing and return colors used + runtime in ms."""
    start = time.perf_counter()
    color_map = simulated_annealing(
        graph,
        initial_temp=initial_temp,
        cooling_rate=cooling_rate,
        max_iter=max_iter,
    )
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
