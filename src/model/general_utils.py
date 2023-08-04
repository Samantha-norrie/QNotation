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

def non_starting_initialize_operation(qc):
    data = qc.data
    non_init_gate_found = False
    for i in range(0, len(data)):
        if not non_init_gate_found and data[i].operation.name != "initialize":
            non_init_gate_found = True
        elif non_init_gate_found and data[i].operation.name == "initialize":
            return True
    return False

def check_qc(qc):

    if qc.num_qubits + qc.num_clbits > 3:
        raise ValueError("Please input a quantum circuit with at most 3 bits.")
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

def add_identity_matrices_to_latex_gate(gate_in_latex, qubits_used_by_gate, num_qubits_in_circuit, dirac=False):
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

                
            
            if i < num_qubits_in_circuit-1 :#and not qubits_used_by_gate.count(num_qubits_in_circuit-1):
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

            if (not qubits_used_by_gate.count(i) or i == qubits_used_by_gate[-1]) and i < num_qubits_in_circuit-1:#and not qubits_used_by_gate.count(num_qubits_in_circuit-1):
                latex_string = latex_string + ' \otimes '
        latex_string = latex_string + '$'
        return latex_string

    # multiple qubit gate with non sequential qubits
    for i in range(0, num_qubits_in_circuit):
        if qubits_used_by_gate.count(i) and not gate_added:
            latex_string = latex_string + gate_in_latex

            gate_added = True
        elif not (i > qubits_used_by_gate[0] and i < qubits_used_by_gate[-1]) and not qubits_used_by_gate.count(i):
            if dirac:
                latex_string = latex_string + IDENTITY_DIRAC
            else:
                latex_string = latex_string + IDENTITY_MATRIX

        if (not qubits_used_by_gate.count(i) or i == qubits_used_by_gate[-1]) and not (i > qubits_used_by_gate[0] and i < qubits_used_by_gate[-1]) and i < num_qubits_in_circuit-1:#and not qubits_used_by_gate.count(num_qubits_in_circuit-1):
            latex_string = latex_string + ' \otimes '
    latex_string = latex_string + '$'
    return latex_string
