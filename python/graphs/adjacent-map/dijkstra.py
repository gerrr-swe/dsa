from graph import Graph
import heapq


def dijkstra(G: Graph, s: Graph.Vertex) -> dict[Graph.Vertex, int]:
    pq : tuple[int,Graph.Vertex] = []
    distance : dict[Graph.Vertex,int] = {}

    heapq.heappush(pq, (0,s))

    for v in G.vertices():
        if v is s:
            distance[v] = 0
        else:
            distance[v] = float("inf")

    while pq:
        d,v = heapq.heappop(pq)

        if d > distance[v]:
            continue

        for e in G.incident_edges(v):
            u = e.opposite(v)
            if distance[u] > e.element() + d:
                distance[u] = e.element() + d
                heapq.heappush(pq,(distance[u],u))

    return distance
