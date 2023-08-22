from qiskit import QuantumCircuit, QuantumRegister
from qiskit.quantum_info import Statevector
from qiskit.quantum_info.operators import Operator
from io import BytesIO
from binascii import b2a_base64
from PIL import Image
import os
import shutil
import matplotlib.pyplot as plt
import numpy as np

SELECTED_COLOUR = '#f05400'
IDENTITY_MATRIX = '\\begin{bmatrix}\n 1 & 0 \\ 0 & 1 \\\\\n\\end{bmatrix}'
IDENTITY_DIRAC = 'I'
PI = np.pi
PARENT_DIRECTORY = os.getcwd()

def format_name_with_angle_value(name, angle_value):
    if angle_value == PI/2.0:
        return name + "(\pi/2)"
    elif angle_value == PI/4.0:
        return name + "(\pi/4)"
    elif angle_value == PI/8.0:
        return name + "(\pi/8)"
    
    return "(" + str(round(angle_value, 3)) + ")"

def create_starting_state_images(qc):
    qc_temp = QuantumCircuit(qc.num_clbits+qc.num_qubits)
    for i in range(0, len(qc)):
        if qc.data[i].operation.name != 'initialize':
            break
        else:
            qc_temp.data.append(qc.data[i])

    directory_starting_states = "starting_states"
    
    path_starting_states = os.path.join(PARENT_DIRECTORY, directory_starting_states)
    if os.path.exists(path_starting_states):
        shutil.rmtree(path_starting_states)
    os.mkdir(path_starting_states) 

    # Dirac
    latex_src = '$' + Statevector(qc_temp).reverse_qargs().draw(output='latex_source') + '$'

    fig, ax = plt.subplots()
    ax.text(0.5, 0.5, latex_src, fontsize=80, ha='center', va='center', transform=ax.transAxes)
    ax.axis('off')
    plt.savefig(path_starting_states + '/dirac_not_selected.svg', dpi=300, bbox_inches='tight')
    plt.close()

    fig, ax = plt.subplots()
    ax.text(0.5, 0.5, latex_src, fontsize=80, ha='center', va='center', transform=ax.transAxes, color=SELECTED_COLOUR)
    ax.axis('off')
    plt.savefig(path_starting_states + '/dirac_selected.svg', dpi=300, bbox_inches='tight')
    plt.close()

    # TODO Matrix

def non_starting_initialize_operation(qc):
    data = qc.data
    non_init_gate_found = False
    for i in range(0, len(data)):
        if not non_init_gate_found and data[i].operation.name != "initialize":
            non_init_gate_found = True
        elif non_init_gate_found and data[i].operation.name == "initialize":
            return True
    return False

# Check if a valid QuantumCircuit was passed to QNotation
# Currently, a valid QuantumCircuit is defined as a circuit which contains
# no initalize() methods after a unitary operator and has no more than 3
# bits.
def check_qc(qc):

    if qc.num_qubits + qc.num_clbits > 3:
        raise ValueError("""Please input a quantum circuit with at most 3 
            bits.""")
    elif non_starting_initialize_operation(qc):
        raise ValueError("Initilaize op error")

def get_index_list_from_qubits(qubit_list):
    indices = []
    for i in range(0, len(qubit_list)):
        indices.append(qubit_list[i].index)
    return indices

def sequential_qubits(qubits):
    if len(qubits) == 2 and qubits[0] == qubits[1]-1:
        return True
    for i in range(qubits[0], len(qubits)):
        if i != qubits[i]:
            return False
    return True

def add_identity_matrices_to_latex_gate(gate_in_latex, 
        qubits_used_by_gate, num_qubits_in_circuit, dirac=False):
    gate_added = False
    latex_string = '$'

    # Single qubit gate
    if len(qubits_used_by_gate) == 1:
        for i in range(0, num_qubits_in_circuit):
            if qubits_used_by_gate.count(i) and not gate_added:
                latex_string = latex_string + gate_in_latex

                gate_added = True
            elif not qubits_used_by_gate.count(i):
                if dirac:
                    latex_string = latex_string + IDENTITY_DIRAC
                else:
                    latex_string = latex_string + IDENTITY_MATRIX

                
            
            if i < num_qubits_in_circuit-1 :
                latex_string = latex_string + ' \otimes '
        latex_string = latex_string + '$'
        return latex_string
    
    # multiple qubit gate with sequential qubits
    elif sequential_qubits(qubits_used_by_gate):
        for i in range(0, num_qubits_in_circuit):
            if qubits_used_by_gate.count(i) and not gate_added:
                latex_string = latex_string + gate_in_latex

                gate_added = True
            elif not qubits_used_by_gate.count(i):
                if dirac:
                    latex_string = latex_string + IDENTITY_DIRAC
                else:
                    latex_string = latex_string + IDENTITY_MATRIX

            if (not qubits_used_by_gate.count(i) or 
                i == qubits_used_by_gate[-1]) and \
                i < num_qubits_in_circuit-1:
                latex_string = latex_string + ' \otimes '
        latex_string = latex_string + '$'
        return latex_string

    # multiple qubit gate with non sequential qubits
    for i in range(0, num_qubits_in_circuit):
        if qubits_used_by_gate.count(i) and not gate_added:
            latex_string = latex_string + gate_in_latex

            gate_added = True
        elif not (i > qubits_used_by_gate[0] 
                and i < qubits_used_by_gate[-1]) and \
                not qubits_used_by_gate.count(i):
            if dirac:
                latex_string = latex_string + IDENTITY_DIRAC
            else:
                latex_string = latex_string + IDENTITY_MATRIX

        if (not qubits_used_by_gate.count(i) or i == qubits_used_by_gate[-1]) and not (i > qubits_used_by_gate[0] and i < qubits_used_by_gate[-1]) and i < num_qubits_in_circuit-1:#and not qubits_used_by_gate.count(num_qubits_in_circuit-1):
            latex_string = latex_string + ' \otimes '
    latex_string = latex_string + '$'
    return latex_string
