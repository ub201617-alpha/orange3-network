import numpy as np


class NeighbourJoining:
    @staticmethod
    def _get_minimum_element_index(matrix):
        return np.unravel_index(matrix.argmin(), matrix.shape)

    def _calculate_q_value(self, i, j):
        matrix = self.distances
        return (len(matrix) - 2) * matrix[i][j] - sum(matrix[i]) - sum(matrix[j])

    def _calculate_q_matrix(self):
        n = len(self.distances)
        q = np.zeros(shape=(n, n))
        for i in range(0, n):
            for j in range(0, n):
                if i != j:
                    q[i][j] = self._calculate_q_value(i, j)
        return q

    def _calculate_new_distances(self, old_indexes, min_x, min_y):
        distances = self.distances
        n = len(distances)
        result = np.zeros(shape=(n - 1, n - 1))
        for i in range(0, len(old_indexes)):
            for j in range(0, len(old_indexes)):
                if i != j:
                    result[i + 1][j + 1] = distances[old_indexes[i]][old_indexes[j]]

        for i in range(0, len(old_indexes)):
            d = 0.5 * (distances[min_x][old_indexes[i]] + distances[min_y][old_indexes[i]] - distances[min_x][min_y])
            result[0][i + 1] = d
            result[i + 1][0] = d
        return result

    def _join_neighbours(self):
        distances = self.distances

        q_matrix = self._calculate_q_matrix()

        min_x, min_y = self._get_minimum_element_index(q_matrix)
        n = len(distances)
        fu = (0.5 * distances[min_x][min_y] + 1 / (2 * (n - 2)) * (sum(distances[min_x]) - sum(distances[min_y])))
        gu = distances[min_x][min_y] - fu

        old_indexes = list(range(0, n))
        old_indexes.remove(min_x)
        old_indexes.remove(min_y)

        new_matrix = self._calculate_new_distances(old_indexes, min_x, min_y)

        # Add new node that will join min_x and min_y
        new_node = self.get_new_node_name()
        self.nodes.append(new_node)
        # TODO Some weird magic, because we're not keeping track of history. Make better!
        if min_x:
            # If min_x is not 0 it means we are adding two leaf nodes (I think)
            self.last_removed = min_x
            just_removed = min_x
        else:
            # If min_x == 0 , we're adding to existing graph
            just_removed = self.last_removed
            self.last_removed = new_node

        # Save new edges and save the calculated distance for them
        self.edges[(new_node, just_removed)] = fu
        self.edges[(new_node, min_y + self.removed)] = gu

        # TODO this is some basic (and wrong) way to adjust for missing indexes
        self.removed += 1
        return (min_x, min_y), new_matrix

    def get_final_graph(self):
        """Run self._join_neighbours until we get a full graph
        """
        while len(self.distances) > 2:
            (min_x, min_y), self.distances = self._join_neighbours()
        self.edges[]

        # TODO we need to add the final edge, but can't do so without first implementing some history tracking
        return self.distances

    def get_all_nodes(self):
        return self.nodes

    def get_all_edges(self):
        return self.edges

    def __init__(self, data):
        self.distances = data
        self.initial_distances = data
        # TODO probably not the best naming -- if input is DistMatrix, we can use labels for node naming
        # But then again, output won't accept anything other than indexes
        self.nodes = list(range(len(self.distances)))
        # Because we'll be changing self.distances, we need to keep track of what's what
        # TODO this is just a naive implementation, that won't work all of the time
        self.removed = 0
        self.last_removed = 0
        self.edges = {}

    def get_new_node_name(self):
        # Just use the next index
        return len(self.nodes)

    def __call__(self, *args, **kwargs):
        while len(self.distances) > 2:
            (min_x, min_y), self.distances = self._join_neighbours()
            yield (min_x, min_y), self.distances


if __name__ == '__main__':
    test_distances = [[0, 5, 9, 9, 8],
                      [5, 0, 10, 10, 9],
                      [9, 10, 0, 8, 7],
                      [9, 10, 8, 0, 3],
                      [8, 9, 7, 3, 0]]
    nj = NeighbourJoining(data=test_distances)
    nj_generator = nj()

    for (x, y), result_distances in nj_generator:
        print("Joining index ", x, " and ", y)
        print("New distances: \n", result_distances)
