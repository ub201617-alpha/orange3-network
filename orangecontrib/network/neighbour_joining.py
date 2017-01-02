import numpy as np


def q_value(matrix, i, j):
    return (len(matrix) - 2) * matrix[i][j] - sum(matrix[i]) - sum(matrix[j])


def minimum_element_index(matrix):
    return np.unravel_index(matrix.argmin(), matrix.shape)


def calculate_q(distances):
    n = len(distances)
    q = np.zeros(shape=(n, n))
    for i in range(0, n):
        for j in range(0, n):
            if i != j:
                q[i][j] = q_value(distances, i, j)
    return q


def calculate_new_distances(distances, old_indexes, min_x, min_y):
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


def join_neighbours(distances):
    print("Initial matrix:\n", distances)

    q_matrix = calculate_q(distances)
    print("Q matrix:\n", q_matrix)

    min_x, min_y = minimum_element_index(q_matrix)
    print("Joining index ", min_x, " and ", min_y)
    n = len(distances)
    fu = (0.5 * distances[min_x][min_y] + 1 / (2 * (n - 2)) * (sum(distances[min_x]) - sum(distances[min_y])))
    gu = distances[min_x][min_y] - fu

    old_indexes = list(range(0, n))
    old_indexes.remove(min_x)
    old_indexes.remove(min_y)

    new_matrix = calculate_new_distances(distances, old_indexes, min_x, min_y)
    print("Final matrix: \n", new_matrix)
    return new_matrix


distances = [[0, 5, 9, 9, 8],
             [5, 0, 10, 10, 9],
             [9, 10, 0, 8, 7],
             [9,	10,	8, 0, 3],
             [8, 9, 7, 3, 0]]
while len(distances) > 2:
    distances = join_neighbours(distances)
