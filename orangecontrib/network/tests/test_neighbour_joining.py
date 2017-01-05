import unittest
import numpy
from orangecontrib.network.neighbour_joining import NeighbourJoining


class TestNeighbourJoining(unittest.TestCase):
    def setUp(self):
        self.distances = [[0, 5, 9, 9, 8],
                          [5, 0, 10, 10, 9],
                          [9, 10, 0, 8, 7],
                          [9, 10, 8, 0, 3],
                          [8, 9, 7, 3, 0]]

    def test_join_neighbours(self):
        nj = NeighbourJoining(self.distances)
        nj_generator = nj()

        test_data_step_1 = [[0, 7, 7, 6],
                            [7, 0, 8, 7],
                            [7, 8, 0, 3],
                            [6, 7, 3, 0]]
        test_joined_step1 = (0, 1)

        joined_idx, out_step_1 = next(nj_generator)
        numpy.testing.assert_array_equal(test_data_step_1, out_step_1)
        self.assertEqual(joined_idx, test_joined_step1)

        test_data_step_2 = [[0, 4, 3],
                            [4, 0, 3],
                            [3, 3, 0]]
        test_joined_step2 = (0, 1)

        joined_idx, out_step_2 = next(nj_generator)
        numpy.testing.assert_array_equal(test_data_step_2, out_step_2)
        self.assertEqual(joined_idx, test_joined_step2)

        test_data_step_3 = [[0, 1],
                            [1, 0]]
        test_joined_step3 = (0, 1)

        joined_idx, out_step_3 = next(nj_generator)
        numpy.testing.assert_array_equal(test_data_step_3, out_step_3)
        self.assertEqual(joined_idx, test_joined_step3)
