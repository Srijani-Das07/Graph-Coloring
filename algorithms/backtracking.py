"""
Backtracking with forward checking for graph coloring.
Vertices ordered by descending degree. Forward checking prunes branches
where any uncolored neighbor has no valid colors remaining.
Time complexity: O(k^V) worst case — feasible up to ~n=50 with pruning.
"""
import time


def _order_vertices(graph):
    return sorted(graph.nodes(), key=lambda v: graph.degree(v), reverse=True)


def _is_safe(graph, vertex, color, color_map):
    return all(color_map.get(nb) != color for nb in graph.neighbors(vertex))


def _forward_check(graph, vertex, color, color_map, k):
    """After assigning color to vertex, check all uncolored neighbors
    still have at least one valid color. Returns False if any neighbor
    is left with no options."""
    for nb in graph.neighbors(vertex):
        if nb in color_map:
            continue
        used = {color_map[n] for n in graph.neighbors(nb) if n in color_map}
        if len(used) >= k:
            return False
    return True


def _backtrack(graph, vertices, color_map, k, index):
    if index == len(vertices):
        return True

    vertex = vertices[index]

    for color in range(k):
        if _is_safe(graph, vertex, color, color_map):
            color_map[vertex] = color
            if _forward_check(graph, vertex, color, color_map, k):
                if _backtrack(graph, vertices, color_map, k, index + 1):
                    return True
            del color_map[vertex]

    return False


def backtracking_coloring(graph):
    vertices = _order_vertices(graph)
    greedy = {}
    for v in vertices:
        used = {greedy[nb] for nb in graph.neighbors(v) if nb in greedy}
        c = 0
        while c in used:
            c += 1
        greedy[v] = c
    k = len(set(greedy.values()))

    color_map = {}
    if _backtrack(graph, vertices, color_map, k, 0):
        return color_map
    return greedy  


def run(graph):
    """Run backtracking. Returns (color_map or None, num_colors or None, runtime_ms)."""
    start = time.perf_counter()
    color_map = backtracking_coloring(graph)
    runtime = (time.perf_counter() - start) * 1000

    if color_map is None:
        return None, None, runtime
    return color_map, len(set(color_map.values())), runtime