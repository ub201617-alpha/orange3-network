from AnyQt.QtWidgets import QLayout
from Orange.misc import DistMatrix
from Orange.widgets.gui import auto_commit
from Orange.widgets.settings import Setting
from Orange.widgets.widget import OWWidget
from orangecontrib.network import Graph


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

    def __init__(self):
        super().__init__()
        self._input_distances = None
        self._setup_layout()

    def _setup_layout(self):
        self.controlArea.setMinimumWidth(self.controlArea.sizeHint().width())
        self.layout().setSizeConstraint(QLayout.SetFixedSize)

        auto_commit(
            widget=self.controlArea,
            master=self,
            value="_auto_apply",
            label="Apply",
            checkbox_label="Auto Apply",
            commit=self.commit
        )

    def set_input_distances(self):
        # todo
        pass

    def commit(self):
        # todo
        pass


if __name__ == '__main__':
    import sys
    from AnyQt.QtWidgets import QApplication
    app = QApplication(sys.argv)
    widget = OWNeighbourJoining()
    widget.show()
    app.exec()
    widget.saveSettings()
