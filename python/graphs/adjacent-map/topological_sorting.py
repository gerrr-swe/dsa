from collections import deque
from graph import Graph


def topological_sorting(G: Graph):
    sorted: list[Graph.Vertex] = []
    next: deque[Graph.Vertex] = deque()
    incount: dict[Graph.Vertex, int] = {}

    for v in G.vertices():
        count = G.degree(v, False)
        incount[v] = count
        if count == 0:
            next.append(v)

    while next:
        v = next.popleft()
        sorted.append(v)
        for e in G.incident_edges(v):
            u = e.opposite(v)
            incount[u] -= 1
            if incount[u] == 0:
                next.append(u)
    return sorted
