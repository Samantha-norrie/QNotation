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

# Matrix functions

def convert_operator_to_latex_src(operator):
    # Convert the NumPy array to a string representation
    arr_str = np.array2string(operator.data, separator=' ')

    # Remove the opening and closing brackets
    arr_str = arr_str.strip('[]')

    # Replace spaces with LaTeX column separators (&)
    arr_str = arr_str.replace(' ', ' & ')

    # Add LaTeX array delimiters and line breaks
    latex_code = '\\begin{bmatrix}\n' + arr_str + ' \\\\\n\\end{bmatrix}'

    return latex_code

def convert_operator_to_latex_matrix(operator):
    data = operator.data
    numpy_matrix = np.matrix(data)
    return Matrix(numpy_matrix, mtype='b')

def get_latex_src(qc):
    latex_src_list = []
    for i in range(0, len(qc.data)):
        if qc.data[i].operation.name != 'barrier':
            latex_src_list.append(convert_operator_to_latex_matrix(Operator(qc.data[i].operation)))
        else: 
            latex_src_list.append('?')

    return latex_src_list

def create_matrix_equation_images(qc):
    parent_directory = os.getcwd()
    directory_matrix = "matrix"
    path_matrix  = os.path.join(parent_directory, directory_matrix )
    if os.path.exists(path_matrix):
        shutil.rmtree(path_matrix )
    os.mkdir(path_matrix)

    data = qc.data

    for i in range(0, len(data)):

        # TODO rename... refactor...
        instance_path = os.path.join(path_matrix, str(i))
        os.mkdir(instance_path) 

        if i%2==0:
            continue

        # Add identity matrices
        gate_formatted_latex_src = add_identity_matrices_to_latex_gate(data[i].operation.name, get_index_list_from_qubits(data[i].qubits), qc.num_qubits)

        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, gate_formatted_latex_src, fontsize=80, ha='center', va='center', transform=ax.transAxes)
        ax.axis('off')
        plt.savefig(instance_path + '/not_selected.png', dpi=300, bbox_inches='tight')
        plt.close()

        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, gate_formatted_latex_src, fontsize=80, ha='center', va='center', transform=ax.transAxes, color=SELECTED_COLOUR)
        ax.axis('off')
        plt.savefig(instance_path + '/selected.png', dpi=300, bbox_inches='tight')
        plt.close()





