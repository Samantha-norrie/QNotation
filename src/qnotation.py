from qiskit import QuantumCircuit
from model.circuit_utils import *
from model.dirac_utils import *
from model.matrix_utils import *
from model.general_utils import *
from view.widget_container import *
from IPython.display import display, clear_output
import os
import get_ipython from IPython
class QNotation:
    @classmethod
    def view_notations(cls, qc: QuantumCircuit):
        # os._exit(00)
        get_ipython().kernel.do_shutdown()
        cls.view = LoadingContainer()
        display(cls.view)
        try:
            check_qc(qc)

        except Exception as error:
            clear_output()
            cls.view = ErrorContainer(error.value)
            display(cls.view)
   
        else: 

            # TODO fix local storage issue, clean this up
            qc_with_barriers = create_highlighted_circuit_figures(qc)
            create_circuit_barrier_images(qc.num_clbits+qc.num_qubits)

            create_starting_state_images(qc)
            create_dirac_state_images(qc, qc_with_barriers)
            create_dirac_equation_images(qc_with_barriers)

            create_matrix_equation_images(qc_with_barriers)
            # clear_output()
            cls.view = WidgetContainer(qc, qc_with_barriers)
            display(cls.view)

