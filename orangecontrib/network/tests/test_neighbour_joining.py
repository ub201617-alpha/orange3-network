import unittest
import numpy
from orangecontrib.network.neighbour_joining import join_neighbours


class TestNeighbourJoining(unittest.TestCase):
    def setUp(self):
        self.distances = [[0, 5, 9, 9, 8],
                          [5, 0, 10, 10, 9],
                          [9, 10, 0, 8, 7],
                          [9, 10, 8, 0, 3],
                          [8, 9, 7, 3, 0]]

    def test_join_neighbours(self):
        test_data_step_1 = [[0, 7, 7, 6],
                            [7, 0, 8, 7],
                            [7, 8, 0, 3],
                            [6, 7, 3, 0]]
        out_step_1 = join_neighbours(self.distances)
        numpy.testing.assert_array_equal(test_data_step_1, out_step_1)

        test_data_step_2 = [[0, 4, 3],
                            [4, 0, 3],
                            [3, 3, 0]]
        out_step_2 = join_neighbours(out_step_1)
        numpy.testing.assert_array_equal(test_data_step_2, out_step_2)

        test_data_step_3 = [[0, 1],
                            [1, 0]]
        out_step_3 = join_neighbours(out_step_2)
        numpy.testing.assert_array_equal(test_data_step_3, out_step_3)
