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
        qc_with_barriers = create_highlighted_circuit_figures(qc)
        create_circuit_barrier_images(qc.num_clbits+qc.num_qubits)

        create_dirac_state_images(qc, qc_with_barriers)
        create_dirac_equation_images(qc_with_barriers)

        create_matrix_equation_images(qc_with_barriers)
        
        cls.view = Container(qc, qc_with_barriers)
        display(cls.view)

