from AnyQt.QtWidgets import QLayout
from Orange.misc import DistMatrix
from Orange.widgets.gui import auto_commit, widgetBox, widgetLabel
from Orange.widgets.settings import Setting
from Orange.widgets.widget import OWWidget
from orangecontrib.network import Graph

import numpy as np


class _Input:
    DISTANCES = "Distances"


class _Output:
    GRAPH = "Graph"


class OWNeighbourJoining(OWWidget):
    name = "Neighbour Joining"
    description = "Computes a phylogenetic tree from a distance matrix."
    icon = ""
    priority = 6470

    inputs = [(_Input.DISTANCES, DistMatrix, "set_input_distances")]
    outputs = [(_Output.GRAPH, Graph)]

    want_main_area = False
    _auto_apply = Setting(default=True)

    _NO_INPUT_INFO_TEXT = "No data on input."

    def __init__(self):
        super().__init__()
        self._input_distances = None
        self._setup_layout()

    def _setup_layout(self):
        self.controlArea.setMinimumWidth(self.controlArea.sizeHint().width())
        self.layout().setSizeConstraint(QLayout.SetFixedSize)

        widget_box = widgetBox(self.controlArea, "Info")
        self.input_distances_info = widgetLabel(
            widget=widget_box,
            label=self._NO_INPUT_INFO_TEXT
        )

        auto_commit(
            widget=self.controlArea,
            master=self,
            value="_auto_apply",
            label="Apply",
            checkbox_label="Auto Apply",
            commit=self.commit
        )

    def set_input_distances(self, distances):
        if distances is None:
            self.send(_Output.GRAPH, None)
            self.input_distances_info.setText(self._NO_INPUT_INFO_TEXT)
            return

        distances_info_text = (
            "Distance matrix with {:d} rows and {:d} columns on input."
        ).format(
            distances.shape[0],
            distances.shape[1]
        )

        self._input_distances = distances
        self.input_distances_info.setText(distances_info_text)

    def commit(self):
        # todo
        self.join_neighbours(self, _Input)

    def q_value(self, matrix, i, j):
        return (len(matrix) - 2) * matrix[i][j] - sum(matrix[i]) - sum(matrix[j])

    def minimum_element_index(matrix):
        return np.unravel_index(matrix.argmin(), matrix.shape)

    def calculate_q(self, distances):
        n = len(distances)
        q = np.zeros(shape=(n, n))
        for i in range(0, n):
            for j in range(0, n):
                if i != j:
                    q[i][j] = self.q_value(distances, i, j)
        return q

    def calculate_new_distances(self, distances, old_indexes, min_x, min_y):
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

    def join_neighbours(self, distances):
        print("Initial matrix:\n", distances)

        q_matrix = self.calculate_q(distances)
        print("Q matrix:\n", q_matrix)

        min_x, min_y = self.minimum_element_index(q_matrix)
        print("Joining index ", min_x, " and ", min_y)
        n = len(distances)
        fu = (0.5 * distances[min_x][min_y] + 1 / (2 * (n - 2)) * (sum(distances[min_x]) - sum(distances[min_y])))
        gu = distances[min_x][min_y] - fu

        old_indexes = list(range(0, n))
        old_indexes.remove(min_x)
        old_indexes.remove(min_y)

        new_matrix = self.calculate_new_distances(distances, old_indexes, min_x, min_y)
        print("Final matrix: \n", new_matrix)
        return new_matrix


if __name__ == '__main__':
    import sys
    from AnyQt.QtWidgets import QApplication
    app = QApplication(sys.argv)
    widget = OWNeighbourJoining()
    widget.show()
    app.exec()
    widget.saveSettings()
