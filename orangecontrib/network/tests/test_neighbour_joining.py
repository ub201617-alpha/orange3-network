import unittest
import numpy
from orangecontrib.network.neighbour_joining import NeighbourJoining


class TestNeighbourJoining(unittest.TestCase):
    def setUp(self):
        # Wikipedia test scenario
        # https://en.wikipedia.org/wiki/Neighbor_joining
        self.distances = [[0, 5, 9, 9, 8],
                          [5, 0, 10, 10, 9],
                          [9, 10, 0, 8, 7],
                          [9, 10, 8, 0, 3],
                          [8, 9, 7, 3, 0]]

        self.test_edges = {(7, 4): 1.0,
                           (7, 3): 2.0,
                           (6, 5): 3.0,
                           (5, 0): 2.0,
                           (6, 2): 4.0,
                           (5, 1): 3.0,
                           (7, 6): 2.0}

    def test_join_neighbours(self):
        nj = NeighbourJoining(self.distances)
        nj.get_final_graph()
        edges = nj.get_all_edges()
        self.assertDictEqual(edges, self.test_edges)
