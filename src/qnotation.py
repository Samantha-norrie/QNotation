from qiskit import QuantumCircuit
from model.circuit_utils import *
from view.widget_container import WidgetContainer
from IPython.display import display

class QNotation:
    @classmethod
    def view_notations(cls, qc: QuantumCircuit):

        # TODO fix local storage issue
        # print(qc)
        create_highlighted_circuit_figures(qc)
        cls.view = WidgetContainer()
        display(cls.view)

