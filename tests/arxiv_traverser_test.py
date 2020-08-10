import unittest
from arxiv_connections import arxiv_util

import networkx as nx

def generate_graph():
    """
    Generate a Graph
    A - B - D - F
    |       | \ |
    C       E - G
    """
    G = nx.Graph()
    G.add_edge("A","B")
    G.add_edge("A","C")
    G.add_edge("B","D")
    G.add_edge("D","F")
    G.add_edge("D","E")
    G.add_edge("D","G")
    G.add_edge("F","G")
    G.add_edge("E","G")
    return G

def _list_equal(l1,l2):
    """ helper, return true if lists are equal"""
    return (len(l1) == len(l2)) and all([l1[i]==l2[i] for i in range(len(l1))])

class TestTask_Arxiv_Traverser(unittest.TestCase):
    def test_BFS(self):
        """ Do a BFS on a known graph, and make sure that the traversal is correct"""
        traversal_tracker = []
        G = generate_graph()
        def next_traversal_f(vertex, traversal_tracker): 
            traversal_tracker.append(vertex)
            return G.neighbors(vertex)
        next_traversal_f_partially_applied = lambda vertex,depth : next_traversal_f(vertex, traversal_tracker) 
        arxiv_util.discovery_BFS_traversal(root="A", max_depth=10,next_traversal_f = next_traversal_f_partially_applied)
        
        expected_options = (["A", "B", "C", "D", "E", "F", "G"], ["A", "C", "B", "D", "E", "F", "G"], ["A", "B", "C", "D", "F", "E", "G"], ["A", "C", "B", "D", "F", "E", "G"])
        
        self.assertTrue(any([_list_equal(traversal_tracker, option) for option in expected_options]))
    
    def test_BFS_max_depth(self):
        """
        Do a BFS on a known graph, and make sure that the traversal is correct
            Test that BFS only goes as far as X depth
        """
        traversal_tracker = []
        G = generate_graph()
        def next_traversal_f(vertex, traversal_tracker): 
            traversal_tracker.append(vertex)
            return G.neighbors(vertex)
        next_traversal_f_partially_applied = lambda vertex, depth: next_traversal_f(vertex, traversal_tracker) 
        arxiv_util.discovery_BFS_traversal(root="A", max_depth=3,next_traversal_f = next_traversal_f_partially_applied)
        
        expected_options = (["A", "B", "C", "D"], ["A", "C", "B", "D"])
        print(traversal_tracker)
        self.assertTrue(any([_list_equal(traversal_tracker, option) for option in expected_options]))
