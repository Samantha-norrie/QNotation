from qiskit import QuantumCircuit
from model.circuit_utils import *
from model.dirac_utils import *
from model.matrix_utils import *
from view.widget_container import Container
from IPython.display import display

class QNotation:
    @classmethod
    def view_notations(cls, qc: QuantumCircuit):

        # TODO fix local storage issue
        # print(qc)
        qc_with_barriers = create_highlighted_circuit_figures(qc)
        create_dirac_state_images(qc, qc_with_barriers)
        # create_matrices_from_circuit(qc)
        cls.view = Container(qc, qc_with_barriers)
        display(cls.view)

