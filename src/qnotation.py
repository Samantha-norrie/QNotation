from qiskit import QuantumCircuit
from model.circuit_utils import *
from view.WidgetContainer import WidgetContainer

class QNotation:
    @classmethod
    def view_notations(cls, qc: QuantumCircuit):
        create_highlighted_circuit_figures(qc)
        
        return True

