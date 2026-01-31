from graph import Graph
from collections import deque


def dfs(
    G: Graph, s: Graph.Vertex, discovered: dict[Graph.Vertex, Graph.Edge], outgoing=True
):
    """Assumes argument discovered[s] = None was added

    Implements DFS using recursion
    Outgoing parameter can be used to act over incoming edges
    """
    incident = G.incident_edges(s, outgoing)
    for edge in incident:
        v = edge.opposite(s)
        if v not in discovered:
            discovered[v] = edge
            dfs(G, v, discovered)


def dfs_stack(G: Graph, s: Graph.Vertex, outgoing=True):
    """Returns a map with the Vertex as key and the Edge used to discover it as value

    Implements DFS using stack
    Outgoing parameter can be used to act over incoming edges
    """
    stack: deque[Graph.Vertex] = deque()
    discovered: dict[Graph.Vertex, Graph.Edge] = {}
    stack.append(s)
    discovered[s] = None

    while stack:
        v = stack.pop()
        incident = G.incident_edges(v, outgoing)
        for edge in incident:
            w = edge.opposite(v)
            if w not in discovered:
                discovered[w] = edge
                stack.append(w)

    return discovered


def construct_path(
    u: Graph.Vertex, v: Graph.Vertex, discovered: dict[Graph.Vertex, Graph.Edge]
):
    """Returns a path from v to u inform of a list of vertices"""
    path = []

    if v in discovered and u in discovered:
        path.append(v)
        curr = v
        while curr is not u:
            edge = discovered[curr]
            parent = edge.opposite(curr)
            path.append(parent)
            curr = parent
    path.reverse()
    return path


def test_connectivity(G: Graph, s: Graph.Vertex):
    """Tests the connectivity of a graph using dfs"""
    out = {s: None}
    dfs(G, s, out)
    if not G.is_directed():
        return len(out) == G.vertex_count()
    inc = {s: None}
    dfs(G, s, inc, False)
    return len(out) == G.vertex_count() and len(inc) == G.vertex_count()


def dfs_complete(G: Graph):
    """Returns a dictionary containing a forest of connected components
    The vertices are keys and the edges used to discover them are values

    The nodes with None values are root nodes
    """
    forest = {}
    for v in G.vertices():
        if v not in forest:
            forest[v] = None
            dfs(G, v, forest)
    return forest


def dfs_has_cycle(G: Graph, s: Graph.Vertex):
    def _search_cycle(s: Graph.Vertex, discovered: dict[Graph.Vertex, Graph.Edge]):
        for e in G.incident_edges(s):
            v = e.opposite(s)
            if v not in discovered:
                discovered[v] = e
                if _search_cycle(v, discovered):
                    return True
            else:
                # ignore the edge leading back to the parent
                if discovered[s] is None or e is not discovered[s]:
                    return True
        return False

    return _search_cycle(s, {s: None})
