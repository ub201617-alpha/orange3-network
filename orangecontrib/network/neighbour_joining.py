import numpy as np


class NeighbourJoining:
    @staticmethod
    def _get_minimum_element_index(matrix):
        return np.unravel_index(np.nanargmin(matrix), matrix.shape)

    def _calculate_q_value(self, i, j):
        matrix = self.distances
        mask = np.all(np.isnan(matrix), axis=1)

        return (len(matrix) - 2 - sum(mask)) * matrix[i][j] - np.nansum(matrix[i]) - np.nansum(matrix[j])

    def _calculate_q_matrix(self):
        n = len(self.distances)
        q = np.zeros(shape=(n, n))
        for i in set(np.where(~np.isnan(self.distances))[0]):
            for j in set(np.where(~np.isnan(self.distances))[1]):
                if i != j:
                    q[i][j] = self._calculate_q_value(i, j)
        return q

    def _calculate_new_distances(self, min_x, min_y):
        distances = self.distances

        joined = np.zeros(distances.shape[0])
        distances = np.vstack((distances, joined))
        joined = np.zeros(distances.shape[0])
        distances = np.column_stack((distances, joined))

        for i in range(0, distances.shape[0] - 1):
            if i != min_x and i != min_y:
                d = 0.5 * (distances[min_x][i] + distances[min_y][i] - distances[min_x][min_y])
                distances[-1][i] = d
                distances[i][-1] = d

        distances[min_x, :] = np.NaN
        distances[:, min_x] = np.NaN
        distances[min_y, :] = np.NaN
        distances[:, min_y] = np.NaN
        return distances

    def _join_neighbours(self):
        distances = self.distances

        q_matrix = self._calculate_q_matrix()
        min_x, min_y = self._get_minimum_element_index(q_matrix)
        n = np.sum(~np.all(np.isnan(distances), axis=1))  # length without nan values

        d_xy = distances[min_x][min_y]
        sum_dx = np.nansum(distances[min_x])
        sum_dy = np.nansum(distances[min_y])
        fu = (0.5 * d_xy + 1 / (2 * (n - 2)) * (sum_dx - sum_dy))
        gu = d_xy - fu

        self.distances = self._calculate_new_distances(min_x, min_y)
        return (min_x, min_y), (fu, gu)

    def get_final_graph(self):
        """Run self._join_neighbours until we get a full graph
        """
        self.__call__()

    def get_all_nodes(self):
        return self.nodes

    def get_all_edges(self):
        return self.edges

    def __init__(self, data):
        N = len(data)
        self.num_of_iterations = N - 3
        self.distances = np.array(data)
        self.max_node = N + self.num_of_iterations
        self.nodes = list(range(N))
        self.nodes.append(self.max_node)
        self.edges = {(self.max_node, i): 0 for i in range(N)}

    def get_new_node_name(self):
        # Just use the next index
        return len(self.nodes)

    def get_num_iterations(self):
        return self.num_of_iterations

    def get_final_graph_progress(self):
        for i in range(self.num_of_iterations):
            self._neighbour_joining_step()
            yield i

        self._neighbour_joining_last_step()
        yield self.num_of_iterations

    def _neighbour_joining_step(self):
        new_node_index = len(self.distances)
        (j1, j2), (d1, d2) = self._join_neighbours()
        self.nodes.append(new_node_index)
        self.edges[(new_node_index, j1)] = d1
        self.edges[(new_node_index, j2)] = d2
        self.edges[(self.max_node, new_node_index)] = 0
        self.edges.pop((self.max_node, j1), None)
        self.edges.pop((self.max_node, j2), None)

    def _neighbour_joining_last_step(self):
        """
        Remaining distances calculation
        """
        (j1, j2), (d1, d2) = self._join_neighbours()
        self.edges[(self.max_node, j1)] = d1
        self.edges[(self.max_node, j2)] = d2
        last_idx, _ = self._get_minimum_element_index(self.distances)
        self.edges[(self.max_node, last_idx)] = self.distances[self.max_node][last_idx]

    def __call__(self, *args, **kwargs):
        for i in range(self.num_of_iterations):
            self._neighbour_joining_step()

        self._neighbour_joining_last_step()


if __name__ == '__main__':
    test_distances = [[0, 5, 9, 9, 8],
                      [5, 0, 10, 10, 9],
                      [9, 10, 0, 8, 7],
                      [9, 10, 8, 0, 3],
                      [8, 9, 7, 3, 0]]

    test_distances1 = [[0, 5, 4, 7, 6, 8],
                       [5, 0, 7, 10, 9, 11],
                       [4, 7, 0, 7, 6, 8],
                       [7, 10, 7, 0, 5, 9],
                       [6, 9, 6, 5, 0, 8],
                       [8, 11, 8, 9, 8, 0]]

    test_distances = np.array(test_distances)
    nj = NeighbourJoining(data=test_distances)
    nj.get_final_graph()
    for edge in nj.get_all_edges():
        print(edge)
