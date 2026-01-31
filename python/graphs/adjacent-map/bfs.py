from graph import Graph
from collections import deque
from copy import deepcopy


def bfs(G: Graph, s: Graph.Vertex, discovered: dict[Graph.Vertex, Graph.Edge]):
    level = [s]

    while level:
        next_level = []
        for u in level:
            for e in G.incident_edges(u):
                v = e.opposite(u)
                if v not in discovered:
                    discovered[v] = e
                    next_level.append(v)
        level = next_level


def bfs_queue(G: Graph, s: Graph.Vertex):
    discovered = {s: None}
    queue = deque()
    queue.append(s)

    while queue:
        v = queue.popleft()
        for e in G.incident_edges(v):
            u = e.opposite(v)
            if u not in discovered:
                discovered[u] = e
                queue.append(u)
    return discovered


def floyd_warshall(G: Graph):
    closure = deepcopy(G)
    vers = list(closure.vertices())
    n = len(vers)

    for k in range(n):
        for i in range(n):
            if i != k and closure.get_edge(vers[i], vers[k]) is not None:
                for j in range(n):
                    if i != j != k and closure.get_edge(vers[k], vers[j]) is not None:
                        if closure.get_edge(vers[i], vers[j]) is None:
                            closure.insert_edge(vers[i], vers[j])
    return closure
