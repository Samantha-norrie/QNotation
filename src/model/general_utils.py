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

def get_index_list_from_qubits(qubit_list):
    indices = []
    for i in range(0, len(qubit_list)):
        indices.append(qubit_list[i].index)
    return indices

def add_identity_matrices_to_latex_gate(gate_in_latex, qubits_used_by_gate, num_qubits_in_circuit, dirac=False):
    gate_added = False
    latex_string = '$'

    for i in range(0, num_qubits_in_circuit):
        if qubits_used_by_gate.count(i) and not gate_added:
            latex_string = latex_string + gate_in_latex

            gate_added = True
        elif not qubits_used_by_gate.count(i):
            if dirac:
                latex_string = latex_string + 'I'
            else:
                latex_string = latex_string + '\\begin{bmatrix}\n 1 & 0 \\ 0 & 1 \\\\\n\\end{bmatrix}'

            
        
        if i < num_qubits_in_circuit-1 and not qubits_used_by_gate.count(num_qubits_in_circuit-1):
            latex_string = latex_string + ' \otimes '
    latex_string = latex_string + '$'

    return latex_string