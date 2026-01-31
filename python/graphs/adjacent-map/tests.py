from functools import reduce
import unittest
from graph import Graph
from dijkstra import dijkstra
import dfs
import bfs
from topological_sorting import topological_sorting


class TestGraphSetup(unittest.TestCase):
    """Test graph creation and basic operations"""

    def setUp(self):
        """Create a simple test graph"""
        self.G = Graph()
        self.vA = self.G.insert_vertex("A")
        self.vB = self.G.insert_vertex("B")
        self.vC = self.G.insert_vertex("C")
        self.vD = self.G.insert_vertex("D")
        self.vE = self.G.insert_vertex("E")
        self.vF = self.G.insert_vertex("F")
        self.vG = self.G.insert_vertex("G")

        self.G.insert_edge(self.vA, self.vB)
        self.G.insert_edge(self.vA, self.vC)
        self.G.insert_edge(self.vB, self.vD)
        self.G.insert_edge(self.vC, self.vE)
        self.G.insert_edge(self.vC, self.vF)
        self.G.insert_edge(self.vF, self.vG)
        self.G.insert_edge(self.vG, self.vA)
        self.G.insert_edge(self.vB, self.vC)

    def test_vertex_count(self):
        """Test graph has correct number of vertices"""
        self.assertEqual(self.G.vertex_count(), 7)

    def test_edge_count(self):
        """Test graph has correct number of edges"""
        self.assertEqual(self.G.edge_count(), 8)

    def test_get_edge(self):
        """Test retrieving edges between vertices"""
        edge = self.G.get_edge(self.vA, self.vB)
        self.assertIsNotNone(edge)
        self.assertEqual(edge.endpoints(), (self.vA, self.vB))

    def test_get_edge_nonexistent(self):
        """Test retrieving nonexistent edge returns None"""
        edge = self.G.get_edge(self.vD, self.vG)
        self.assertIsNone(edge)


class TestDFSRecursive(unittest.TestCase):
    """Test recursive DFS implementation"""

    def setUp(self):
        """Create a simple test graph"""
        self.G = Graph()
        self.vA = self.G.insert_vertex("A")
        self.vB = self.G.insert_vertex("B")
        self.vC = self.G.insert_vertex("C")
        self.vD = self.G.insert_vertex("D")

        self.G.insert_edge(self.vA, self.vB)
        self.G.insert_edge(self.vA, self.vC)
        self.G.insert_edge(self.vB, self.vD)

    def test_dfs_discovers_all_vertices(self):
        """Test that DFS discovers all reachable vertices"""
        discovered = {self.vA: None}
        dfs.dfs(self.G, self.vA, discovered)
        self.assertEqual(len(discovered), 4)
        self.assertIn(self.vA, discovered)
        self.assertIn(self.vB, discovered)
        self.assertIn(self.vC, discovered)
        self.assertIn(self.vD, discovered)

    def test_dfs_partial_graph(self):
        """Test DFS on disconnected graph from specific vertex"""
        G = Graph()
        v1 = G.insert_vertex("1")
        v2 = G.insert_vertex("2")
        v3 = G.insert_vertex("3")
        G.insert_edge(v1, v2)
        # v3 is isolated

        discovered = {v1: None}
        dfs.dfs(G, v1, discovered)
        self.assertEqual(len(discovered), 2)
        self.assertNotIn(v3, discovered)

    def test_dfs_single_vertex(self):
        """Test DFS on single vertex"""
        G = Graph()
        v = G.insert_vertex("X")
        discovered = {v: None}
        dfs.dfs(G, v, discovered)
        self.assertEqual(len(discovered), 1)
        self.assertIn(v, discovered)


class TestDFSStack(unittest.TestCase):
    """Test iterative DFS using stack"""

    def setUp(self):
        """Create a simple test graph"""
        self.G = Graph()
        self.vA = self.G.insert_vertex("A")
        self.vB = self.G.insert_vertex("B")
        self.vC = self.G.insert_vertex("C")
        self.vD = self.G.insert_vertex("D")

        self.G.insert_edge(self.vA, self.vB)
        self.G.insert_edge(self.vA, self.vC)
        self.G.insert_edge(self.vB, self.vD)

    def test_dfs_stack_discovers_all(self):
        """Test that iterative DFS discovers all reachable vertices"""
        discovered = dfs.dfs_stack(self.G, self.vA)
        self.assertEqual(len(discovered), 4)
        self.assertIn(self.vA, discovered)
        self.assertIn(self.vB, discovered)
        self.assertIn(self.vC, discovered)
        self.assertIn(self.vD, discovered)

    def test_dfs_stack_returns_dict(self):
        """Test that DFS stack returns dictionary with None for start vertex"""
        discovered = dfs.dfs_stack(self.G, self.vA)
        self.assertIsNone(discovered[self.vA])
        self.assertIsNotNone(discovered[self.vB])


class TestDFSPath(unittest.TestCase):
    """Test path construction with DFS"""

    def setUp(self):
        """Create a simple test graph"""
        self.G = Graph()
        self.vA = self.G.insert_vertex("A")
        self.vB = self.G.insert_vertex("B")
        self.vC = self.G.insert_vertex("C")
        self.vD = self.G.insert_vertex("D")
        self.vE = self.G.insert_vertex("E")

        self.G.insert_edge(self.vA, self.vB)
        self.G.insert_edge(self.vB, self.vC)
        self.G.insert_edge(self.vC, self.vD)
        self.G.insert_edge(self.vA, self.vE)

    def test_construct_path_exists(self):
        """Test constructing a path between connected vertices"""
        discovered = {self.vA: None}
        dfs.dfs(self.G, self.vA, discovered)
        path = dfs.construct_path(self.vA, self.vD, discovered)
        self.assertEqual(path[0], self.vA)
        self.assertEqual(path[-1], self.vD)
        self.assertTrue(len(path) > 1)

    def test_construct_path_start_end(self):
        """Test path from vertex to itself"""
        discovered = {self.vA: None}
        dfs.dfs(self.G, self.vA, discovered)
        path = dfs.construct_path(self.vA, self.vA, discovered)
        self.assertEqual(path, [self.vA])

    def test_construct_path_unreachable(self):
        """Test path to unreachable vertex"""
        G = Graph()
        v1 = G.insert_vertex("1")
        v2 = G.insert_vertex("2")
        v3 = G.insert_vertex("3")
        G.insert_edge(v1, v2)

        discovered = {v1: None}
        dfs.dfs(G, v1, discovered)
        path = dfs.construct_path(v1, v3, discovered)
        self.assertEqual(path, [])


class TestConnectivity(unittest.TestCase):
    """Test connectivity checking"""

    def test_undirected_connected_graph(self):
        """Test connected undirected graph"""
        G = Graph(False)
        vA = G.insert_vertex("A")
        vB = G.insert_vertex("B")
        vC = G.insert_vertex("C")
        G.insert_edge(vA, vB)
        G.insert_edge(vB, vC)

        self.assertTrue(dfs.test_connectivity(G, vA))

    def test_undirected_disconnected_graph(self):
        """Test disconnected undirected graph"""
        G = Graph(False)
        vA = G.insert_vertex("A")
        vB = G.insert_vertex("B")
        vC = G.insert_vertex("C")
        G.insert_edge(vA, vB)

        self.assertFalse(dfs.test_connectivity(G, vA))

    def test_directed_strongly_connected(self):
        """Test strongly connected directed graph"""
        G = Graph(True)
        vA = G.insert_vertex("A")
        vB = G.insert_vertex("B")
        G.insert_edge(vA, vB)
        G.insert_edge(vB, vA)

        self.assertTrue(dfs.test_connectivity(G, vA))

    def test_directed_not_strongly_connected(self):
        """Test non-strongly connected directed graph"""
        G = Graph(True)
        vA = G.insert_vertex("A")
        vB = G.insert_vertex("B")
        G.insert_edge(vA, vB)

        self.assertFalse(dfs.test_connectivity(G, vA))

    def test_single_vertex_connectivity(self):
        """Test single vertex is connected to itself"""
        G = Graph()
        v = G.insert_vertex("A")
        self.assertTrue(dfs.test_connectivity(G, v))


class TestDFSComplete(unittest.TestCase):
    """Test complete DFS traversal"""

    def test_dfs_complete_connected(self):
        """Test DFS complete on fully connected graph"""
        G = Graph()
        vA = G.insert_vertex("A")
        vB = G.insert_vertex("B")
        vC = G.insert_vertex("C")
        G.insert_edge(vA, vB)
        G.insert_edge(vB, vC)

        forest = dfs.dfs_complete(G)
        self.assertEqual(len(forest), 3)

    def test_dfs_complete_disconnected(self):
        """Test DFS complete on disconnected graph"""
        G = Graph()
        vA = G.insert_vertex("A")
        vB = G.insert_vertex("B")
        vC = G.insert_vertex("C")
        G.insert_edge(vA, vB)

        forest = dfs.dfs_complete(G)
        self.assertEqual(len(forest), 3)
        self.assertIsNone(forest[vA])
        self.assertIsNone(forest[vC])


class TestDFSCycle(unittest.TestCase):
    """Test cycle detection with DFS"""

    def test_graph_with_cycle(self):
        """Test detection of cycle in graph"""
        G = Graph()
        vA = G.insert_vertex("A")
        vB = G.insert_vertex("B")
        vC = G.insert_vertex("C")
        G.insert_edge(vA, vB)
        G.insert_edge(vB, vC)
        G.insert_edge(vC, vA)

        self.assertTrue(dfs.dfs_has_cycle(G, vA))

    def test_graph_without_cycle(self):
        """Test no cycle detection in DAG"""
        G = Graph()
        vA = G.insert_vertex("A")
        vB = G.insert_vertex("B")
        vC = G.insert_vertex("C")
        G.insert_edge(vA, vB)
        G.insert_edge(vB, vC)

        self.assertFalse(dfs.dfs_has_cycle(G, vA))

    def test_self_loop_cycle(self):
        """Test self-loop is detected as cycle"""
        G = Graph()
        v = G.insert_vertex("A")
        G.insert_edge(v, v)

        self.assertTrue(dfs.dfs_has_cycle(G, v))


class TestBFS(unittest.TestCase):
    """Test BFS implementation"""

    def setUp(self):
        """Create a simple test graph"""
        self.G = Graph()
        self.vA = self.G.insert_vertex("A")
        self.vB = self.G.insert_vertex("B")
        self.vC = self.G.insert_vertex("C")
        self.vD = self.G.insert_vertex("D")
        self.vE = self.G.insert_vertex("E")

        self.G.insert_edge(self.vA, self.vB)
        self.G.insert_edge(self.vA, self.vC)
        self.G.insert_edge(self.vB, self.vD)
        self.G.insert_edge(self.vC, self.vE)

    def test_bfs_discovers_all(self):
        """Test BFS discovers all reachable vertices"""
        discovered = {self.vA: None}
        bfs.bfs(self.G, self.vA, discovered)
        self.assertEqual(len(discovered), 5)
        self.assertIn(self.vA, discovered)
        self.assertIn(self.vB, discovered)
        self.assertIn(self.vC, discovered)
        self.assertIn(self.vD, discovered)
        self.assertIn(self.vE, discovered)

    def test_bfs_level_order(self):
        """Test BFS visits vertices level by level"""
        discovered = {self.vA: None}
        bfs.bfs(self.G, self.vA, discovered)
        # A is at level 0, B and C at level 1, D and E at level 2
        self.assertIsNone(discovered[self.vA])
        self.assertIsNotNone(discovered[self.vB])
        self.assertIsNotNone(discovered[self.vC])
        self.assertIsNotNone(discovered[self.vD])
        self.assertIsNotNone(discovered[self.vE])


class TestBFSQueue(unittest.TestCase):
    """Test BFS using queue"""

    def setUp(self):
        """Create a simple test graph"""
        self.G = Graph()
        self.vA = self.G.insert_vertex("A")
        self.vB = self.G.insert_vertex("B")
        self.vC = self.G.insert_vertex("C")
        self.vD = self.G.insert_vertex("D")
        self.vE = self.G.insert_vertex("E")

        self.G.insert_edge(self.vA, self.vB)
        self.G.insert_edge(self.vA, self.vC)
        self.G.insert_edge(self.vB, self.vD)
        self.G.insert_edge(self.vC, self.vE)

    def test_bfs_queue_discovers_all(self):
        """Test queue-based BFS discovers all reachable vertices"""
        discovered = bfs.bfs_queue(self.G, self.vA)
        self.assertEqual(len(discovered), 5)
        self.assertIn(self.vA, discovered)
        self.assertIn(self.vB, discovered)
        self.assertIn(self.vC, discovered)
        self.assertIn(self.vD, discovered)
        self.assertIn(self.vE, discovered)

    def test_bfs_queue_returns_dict(self):
        """Test BFS queue returns proper discovered dictionary"""
        discovered = bfs.bfs_queue(self.G, self.vA)
        self.assertIsNone(discovered[self.vA])
        self.assertIsNotNone(discovered[self.vB])

    def test_bfs_queue_single_vertex(self):
        """Test BFS queue on single vertex"""
        G = Graph()
        v = G.insert_vertex("X")
        discovered = bfs.bfs_queue(G, v)
        self.assertEqual(len(discovered), 1)
        self.assertIn(v, discovered)


class TestFloydWarshall(unittest.TestCase):
    """Test Floyd-Warshall transitive closure algorithm"""

    @staticmethod
    def find_vertex_by_element(graph, element):
        """Helper to find a vertex in a graph by its element value"""
        for v in graph.vertices():
            if v.element() == element:
                return v
        return None

    def test_floyd_warshall_simple(self):
        """Test Floyd-Warshall on simple directed graph"""
        G = Graph(True)
        vA = G.insert_vertex("A")
        vB = G.insert_vertex("B")
        vC = G.insert_vertex("C")
        G.insert_edge(vA, vB)
        G.insert_edge(vB, vC)

        closure = bfs.floyd_warshall(G)

        # Get vertices from closure by their element values
        cA = self.find_vertex_by_element(closure, "A")
        cB = self.find_vertex_by_element(closure, "B")
        cC = self.find_vertex_by_element(closure, "C")

        # After closure: A->B, B->C should add A->C
        self.assertIsNotNone(closure.get_edge(cA, cB))
        self.assertIsNotNone(closure.get_edge(cB, cC))
        self.assertIsNotNone(closure.get_edge(cA, cC))

    def test_floyd_warshall_triangle(self):
        """Test Floyd-Warshall on triangle graph"""
        G = Graph(True)
        vA = G.insert_vertex("A")
        vB = G.insert_vertex("B")
        vC = G.insert_vertex("C")
        G.insert_edge(vA, vB)
        G.insert_edge(vB, vC)
        G.insert_edge(vC, vA)

        closure = bfs.floyd_warshall(G)

        # Get vertices from closure by their element values
        cA = self.find_vertex_by_element(closure, "A")
        cB = self.find_vertex_by_element(closure, "B")
        cC = self.find_vertex_by_element(closure, "C")

        # All vertices should be reachable from all
        for v1 in [cA, cB, cC]:
            for v2 in [cA, cB, cC]:
                if v1 != v2:
                    self.assertIsNotNone(
                        closure.get_edge(v1, v2),
                        f"No edge from {v1.element()} to {v2.element()}",
                    )

    def test_floyd_warshall_no_paths(self):
        """Test Floyd-Warshall on disconnected graph"""
        G = Graph(True)
        vA = G.insert_vertex("A")
        vB = G.insert_vertex("B")
        vC = G.insert_vertex("C")
        G.insert_edge(vA, vB)

        closure = bfs.floyd_warshall(G)

        # Get vertices from closure by their element values
        cA = self.find_vertex_by_element(closure, "A")
        cB = self.find_vertex_by_element(closure, "B")
        cC = self.find_vertex_by_element(closure, "C")

        self.assertIsNotNone(closure.get_edge(cA, cB))
        self.assertIsNone(closure.get_edge(cB, cA))
        self.assertIsNone(closure.get_edge(cA, cC))

    def test_floyd_warshall_single_vertex(self):
        """Test Floyd-Warshall on single vertex"""
        G = Graph(True)
        v = G.insert_vertex("A")

        closure = bfs.floyd_warshall(G)
        self.assertEqual(closure.vertex_count(), 1)

    def test_floyd_warshall_complex(self):
        """Test Floyd-Warshall on more complex graph"""
        G = Graph(True)
        v1 = G.insert_vertex("1")
        v2 = G.insert_vertex("2")
        v3 = G.insert_vertex("3")
        v4 = G.insert_vertex("4")
        G.insert_edge(v1, v2)
        G.insert_edge(v2, v3)
        G.insert_edge(v3, v4)
        G.insert_edge(v2, v4)

        closure = bfs.floyd_warshall(G)

        # Get vertices from closure by their element values
        c1 = self.find_vertex_by_element(closure, "1")
        c2 = self.find_vertex_by_element(closure, "2")
        c3 = self.find_vertex_by_element(closure, "3")
        c4 = self.find_vertex_by_element(closure, "4")

        # Should have transitive closures
        self.assertIsNotNone(closure.get_edge(c1, c2))
        self.assertIsNotNone(closure.get_edge(c1, c3))
        self.assertIsNotNone(closure.get_edge(c1, c4))

class TestTopologicalSort(unittest.TestCase):

    def test_topological_sort_simple_path(self):
        G = Graph(True)
        vA = G.insert_vertex("A")
        vB = G.insert_vertex("B")
        vC = G.insert_vertex("C")
        vD = G.insert_vertex("D")
        vE = G.insert_vertex("E")

        G.insert_edge(vA,vB)
        G.insert_edge(vB,vC)
        G.insert_edge(vC,vD)
        G.insert_edge(vD,vE)

        self.assertEqual([vA,vB,vC,vD,vE],topological_sorting(G))

    def test_topological_sort_simple_path_cycle(self):
        G = Graph(True)
        vA = G.insert_vertex("A")
        vB = G.insert_vertex("B")
        vC = G.insert_vertex("C")
        vD = G.insert_vertex("D")
        vE = G.insert_vertex("E")

        G.insert_edge(vA, vB)
        G.insert_edge(vB, vC)
        G.insert_edge(vC, vD)
        G.insert_edge(vD, vE)
        G.insert_edge(vE, vA)

        self.assertNotEqual(G.vertex_count(), len(topological_sorting(G)))

    def test_topological_sort_complex(self):
        G = Graph(True)
        vA = G.insert_vertex("A")
        vB = G.insert_vertex("B")
        vC = G.insert_vertex("C")
        vD = G.insert_vertex("D")
        vE = G.insert_vertex("E")
        vF = G.insert_vertex("F")
        vG = G.insert_vertex("G")
        vH = G.insert_vertex("H")

        G.insert_edge(vA, vC)
        G.insert_edge(vA, vD)
        G.insert_edge(vB, vD)
        G.insert_edge(vB, vF)
        G.insert_edge(vC, vH)
        G.insert_edge(vC, vE)
        G.insert_edge(vC, vD)
        G.insert_edge(vD, vF)
        G.insert_edge(vE, vG)
        G.insert_edge(vF, vG)
        G.insert_edge(vF, vH)

        self.assertEqual(G.vertex_count(), len(topological_sorting(G)))

    def test_topological_sort_complex_cycle(self):
        G = Graph(True)
        vA = G.insert_vertex("A")
        vB = G.insert_vertex("B")
        vC = G.insert_vertex("C")
        vD = G.insert_vertex("D")
        vE = G.insert_vertex("E")
        vF = G.insert_vertex("F")
        vG = G.insert_vertex("G")
        vH = G.insert_vertex("H")

        G.insert_edge(vA, vC)
        G.insert_edge(vA, vD)
        G.insert_edge(vB, vD)
        G.insert_edge(vB, vF)
        G.insert_edge(vC, vH)
        G.insert_edge(vC, vE)
        G.insert_edge(vC, vD)
        G.insert_edge(vD, vF)
        G.insert_edge(vE, vG)
        G.insert_edge(vF, vG)
        G.insert_edge(vF, vH)
        G.insert_edge(vH, vA)

        self.assertNotEqual(G.vertex_count(), len(topological_sorting(G)))

class Dijkstra(unittest.TestCase):
    def test_dijkstr(self):
        G = Graph()
        v1 = G.insert_vertex(1)
        v2 = G.insert_vertex(2)
        v3 = G.insert_vertex(3)
        v4 = G.insert_vertex(4)
        v5 = G.insert_vertex(5)
        v6 = G.insert_vertex(6)
        v7 = G.insert_vertex(7)
        v8 = G.insert_vertex(8)
        v9 = G.insert_vertex(9)

        G.insert_edge(v2,v5,1)
        G.insert_edge(v1,v2,2)
        G.insert_edge(v2,v3,3)
        G.insert_edge(v1,v3,5)
        G.insert_edge(v3,v5,1)
        G.insert_edge(v3,v8,1)
        G.insert_edge(v8,v9,1)
        G.insert_edge(v5,v9,7)
        G.insert_edge(v4,v1,2)
        G.insert_edge(v4,v3,3)
        G.insert_edge(v6,v3,1)
        G.insert_edge(v6,v8,3)
        G.insert_edge(v7,v4,2)
        G.insert_edge(v7,v6,2)

        distance = dijkstra(G, v1)

        self.assertEqual(distance[v1],0)
        self.assertEqual(distance[v2],2)
        self.assertEqual(distance[v3],4)
        self.assertEqual(distance[v4],2)
        self.assertEqual(distance[v5],3)
        self.assertEqual(distance[v6],5)
        self.assertEqual(distance[v7],4)
        self.assertEqual(distance[v8],5)
        self.assertEqual(distance[v9],6)

if __name__ == "__main__":
    unittest.main()
