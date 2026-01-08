class Vertex:
    """Lightweight vertex structure for a graph"""

    __slots__ = "_element"

    def __init__(self, x):
        """Do not use constructor, use instead Graph.insert_vertex(x)"""
        self._element = x

    def element(self):
        """Return the element associated with the vertex"""
        return self._element

    def __hash__(self):
        return hash(id(self))


class Edge:
    """Lightweight edge structure for a graph"""

    __slots__ = ["u", "v", "x"]

    def __init__(self, u, v, x):
        """Do not use constructor, use instead Graph.insert_edge(u,v,x)"""
        self._origin = u
        self._destination = v
        self._element = x

    def endpoints(self):
        """Return (u,v) typle for vertices u and v"""
        return (self._origin, self._destination)

    def element(self):
        """Return the element associated with the edge"""
        return self._element

    def __hash__(self):
        return hash((self._origin, self._destination))


class Graph:

    def __init__(self, directed=False):
        self._outgoing = {}
        self._incoming = {} if directed else self._outgoing

    def is_directed(self):
        return self._outgoing is not self._incoming

    def vertex_count(self):
        return len(self._outgoing)

    def vertices(self):
        return self._outgoing.keys()
