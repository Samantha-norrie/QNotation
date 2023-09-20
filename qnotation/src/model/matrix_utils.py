import reacton
import reacton.ipyvuetify as rv
import reacton.ipywidgets as w

from qiskit import QuantumCircuit, QuantumRegister
from qiskit.quantum_info import Statevector
from qiskit.quantum_info.operators import Operator
import ipywidgets as widgets
from IPython.display import HTML
from io import BytesIO
from binascii import b2a_base64
from PIL import Image
import os
import shutil
import matplotlib.pyplot as plt
from model.general_utils import *
import numpy as np
from pdf2image import convert_from_path
from pylatex import Document, Section, Subsection, Tabular, Math, TikZ, Axis, \
    Plot, Figure, Matrix, Alignat, Command
from pylatex.utils import italic
import sympy
from tabulate import tabulate
from sympy.physics.quantum import TensorProduct
from sympy import Matrix

TABULATE_FORMAT = "presto"
IDENTITY_MATRIX = Matrix([[1.0, 0.0],
        [0.0,1.0]])


# Matrix functions
def format_matrix_values(matrix):
    for i in range(0, len(matrix)):
        for j in range(0, len(matrix[i])):
            # print(matrix[i][j].real, matrix[i][j].imag, matrix[i][j].conjugate())
            if matrix[i][j].imag == 0.0:
                matrix[i][j] = round(matrix[i][j].real, 2)
            elif matrix[i][j].real == 0.0 and matrix[i][j].imag == 1.0:
                matrix[i][j] = 'i'
    return matrix

def compute_operation_matrix(matrix, qubits_used_by_gate, num_qubits_in_circuit):

    matrix_added = False
    m = IDENTITY_MATRIX.copy()
    if qubits_used_by_gate.count(num_qubits_in_circuit-1):
        m = matrix
        matrix_added = True

    for i in range(num_qubits_in_circuit-2, -1, -1):
        if not qubits_used_by_gate.count(i):
            m = TensorProduct(IDENTITY_MATRIX, m)
        elif qubits_used_by_gate.count(i) and not matrix_added:
            m = TensorProduct(matrix, m)
            matrix_added = True

    return m.tolist()

def create_matrix_state_images(qc_orig, qc_barriers):
    parent_directory = os.getcwd()
    directory_matrix = "matrix"
    
    path_matrix = os.path.join(parent_directory, directory_matrix)
    if os.path.exists(path_matrix):
        shutil.rmtree(path_matrix)
    os.mkdir(path_matrix)
    qc_rev = qc_orig.reverse_bits()

    img_num = 1
    for i in range(1, len(qc_rev.data)+1):
        temp_circuit = QuantumCircuit(qc_rev.num_qubits)
        new_data = []
        for j in range(0, i):
            new_data.append(qc_rev.data[j])
        temp_circuit.data = new_data 

        starting_vector = list_to_tabulate_vector(Statevector(temp_circuit).reverse_qargs().probabilities().tolist())
        # print(starting_vector)
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, tabulate(starting_vector, TABULATE_FORMAT), fontsize=120, ha='center', va='center', transform=ax.transAxes, color=SELECTED_COLOUR)
        ax.axis('off')
        plt.savefig(path_matrix + '/' + str(img_num)+'.png', dpi=300, bbox_inches='tight')
        plt.close()

        img_num = img_num+2

def create_matrix_equation_images_tabulate(qc):
    parent_directory = os.getcwd()
    directory_matrix = "matrix_equations"
    path_matrix  = os.path.join(parent_directory, directory_matrix )
    if os.path.exists(path_matrix):
        shutil.rmtree(path_matrix )
    os.mkdir(path_matrix)

    init_gates = number_of_init_gates(qc)

    op_number = 0
    for i in range(init_gates, len(qc.data)):
        instance_path = os.path.join(directory_matrix, str(op_number))
        os.mkdir(instance_path) 
        temp_circuit = QuantumCircuit(qc.num_qubits + qc.num_clbits)
        new_data = []
        for j in range(init_gates, i):
            new_data.append(qc.data[j])
        temp_circuit.data = new_data

        #TODO a little bit of cleaning
        matrix = compute_operation_matrix(Matrix(format_matrix_values(Operator(qc.data[i].operation).data.tolist())), get_index_list_from_qubits(qc.data[i].qubits), qc.num_qubits)

        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, tabulate(matrix, tablefmt=TABULATE_FORMAT), fontsize=80, ha='center', va='center', transform=ax.transAxes)
        ax.axis('off')
        plt.savefig(instance_path + '/not_selected.svg', dpi=300, bbox_inches='tight')
        plt.close()

        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, tabulate(matrix, tablefmt=TABULATE_FORMAT), fontsize=80, ha='center', va='center', transform=ax.transAxes, color=SELECTED_COLOUR)
        ax.axis('off')
        plt.savefig(instance_path + '/selected.svg', dpi=300, bbox_inches='tight')
        plt.close()

        op_number=op_number+2





