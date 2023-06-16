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
plt.rcParams['text.usetex'] = True

import numpy as np
from pdf2image import convert_from_path

from pylatex import Document, Section, Subsection, Tabular, Math, TikZ, Axis, \
    Plot, Figure, Matrix, Alignat, Command
from pylatex.utils import italic
import sympy

# Matrix functions

IDENTITY_MATRIX = Matrix(np.matrix([[1,0],[0,1]]), mtype='b')

def convert_operator_to_latex_matrix(operator):
    data = operator.data
    numpy_matrix = np.matrix(data)
    return Matrix(numpy_matrix, mtype='b')

def get_latex_matrices(qc):
    matrices = []
    for i in range(0, len(qc.data)):
        if qc.data[i].operation.name != 'barrier':
            matrices.append(convert_operator_to_latex_matrix(Operator(qc.data[i].operation)))
    return matrices

def create_matrices_from_circuit(qc):
    parent_directory = os.getcwd()
    directory_matrix = "matrix"
    path_matrix  = os.path.join(parent_directory, directory_matrix )
    if os.path.exists(path_matrix):
        shutil.rmtree(path_matrix )
    os.mkdir(path_matrix ) 

    matrices = get_latex_matrices(qc)
    for i in range(0, len(matrices)):
        doc = Document()
        doc.documentclass = Command(
        'documentclass',
        options=['12pt', 'landscape'],
        arguments=['standalone'],
    )
        math = Math(data=[IDENTITY_MATRIX, 'x', matrices[i]])
        doc.append(math)

        # TODO fix local storage issue
        doc.generate_pdf(str(i))
        img = convert_from_path(str(i)+'.pdf')
        img.save('./'+ directory_matrix+ '/'+str(i) +'.png', 'PNG')
        os.remove(str(i) +'.pdf')





