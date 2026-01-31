from __future__ import annotations
from typing import Any


class Graph:

    class Vertex:
        """Lightweight vertex structure for a graph"""

        __slots__ = "_element"

        def __init__(self, x: Any):
            """Do not use constructor, use instead Graph.insert_vertex(x)"""
            self._element = x

        def element(self):
            """Return the element associated with the vertex"""
            return self._element

        def __hash__(self):
            return hash(id(self))

        def __str__(self):
            return f"Vertex Element: {self.element()}"

        def __repr__(self):
            return f"Vertex Element: {self.element()}"
        
        def __lt__(self,other):
            if isinstance(other,Graph.Vertex):
                return self._element < other._element
            return NotImplemented




    class Edge:
        """Lightweight edge structure for a graph"""

        __slots__ = ["_origin", "_destination", "_element"]

        def __init__(self, u: Graph.Vertex, v: Graph.Vertex, x: Any):
            """Do not use constructor, use instead Graph.insert_edge(u,v,x)"""
            self._origin = u
            self._destination = v
            self._element = x

        def endpoints(self):
            """Return (u,v) typle for vertices u and v"""
            return (self._origin, self._destination)

        def opposite(self, v):
            """Returns the opposite vertex to v in the edge"""
            return self._destination if v is self._origin else self._origin

        def element(self):
            """Return the element associated with the edge"""
            return self._element

        def __hash__(self):
            return hash((self._origin, self._destination))

        def __str__(self):
            return f"Edge Element {self.endpoints()}: {self.element()}"

        def __repr__(self):
            return f"Edge Element {self.endpoints()}: {self.element()}"

    def __init__(self, directed=False):
        self._outgoing: dict[Graph.Vertex, dict[Graph.Vertex, Graph.Edge]] = {}
        self._incoming: dict[Graph.Vertex, dict[Graph.Vertex, Graph.Edge]] = (
            {} if directed else self._outgoing
        )

    def is_directed(self):
        """Returns True if the graph is directed"""
        return self._outgoing is not self._incoming

    def vertex_count(self):
        """Returns the number of vertices in the graph"""
        return len(self._outgoing)

    def vertices(self):
        """Returns an iteration of all the vertices present in the graph"""
        return self._outgoing.keys()

    def edge_count(self):
        """Returns the number of edges in the graph"""
        total = sum(len(self._outgoing[v]) for v in self._outgoing)
        # sum of degrees, hand shake lemma
        return total if self.is_directed() else total // 2

    def edges(self):
        """Returns a set of all the edges in the graph"""
        unique: set[Graph.Edge] = set()
        for adjs in self._outgoing.values():
            unique.update(adjs.values())
        return unique

    def get_edge(self, u: Vertex, v: Vertex):
        """Returns the edge (u,v), None if does not exists"""
        return self._outgoing[u].get(v)

    def degree(self, v: Vertex, outgoing=True):
        """Returns the number of outgoing incident edges to the vertex v

        If directed, the optional parameter can give the number of incoming 
        """
        adj = self._outgoing[v] if outgoing else self._incoming
        return len(adj[v])

    def incident_edges(self, v: Vertex, outgoing=True):
        """Returns an iteration of all outgoing incident vertices to a vertex

        If directed, the optional parameter can give the number of incoming
        """
        adj = self._outgoing if outgoing else self._incoming
        for edge in adj[v].values():
            yield edge

    def insert_vertex(self, x=None):
        """Inserts and returns a new vertex into graph with element x"""
        v = self.Vertex(x)
        self._outgoing[v] = {}
        if self.is_directed():
            self._incoming[v] = {}
        return v

    def insert_edge(self, u, v, x=None):
        """Inserts and returns a new edge into the graph with element x"""
        e = self.Edge(u, v, x)
        self._outgoing[u][v] = e
        self._incoming[v][u] = e
        return e
