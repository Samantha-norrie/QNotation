from qiskit import QuantumCircuit, QuantumRegister
from qiskit.quantum_info import Statevector
from io import BytesIO
from binascii import b2a_base64
from PIL import Image
import os
import shutil
import matplotlib.pyplot as plt
plt.rcParams['text.usetex'] = True

import numpy as np

from pylatex import Document, Section, Subsection, Tabular, Math, TikZ, Axis, \
    Plot, Figure, Matrix, Alignat
from pylatex.utils import italic
import sympy

# Statevector functions
def get_barrier_states(qc, num_qubits):
    states = []
    
    for i in range(0, len(qc.data)):
        temp_circuit = QuantumCircuit(num_qubits)
        new_data = []
        for j in range(0, i):
            new_data.append(qc.data[j])
        temp_circuit.data = new_data
        states.append(Statevector(temp_circuit).draw(output='latex_source'))
    return states

def compile_latex_src_dirac_states(qc, barrier_states):
    latex_src_dirac_states = []
    current_barrier_state_index = 0

    for i in range(0, len(qc)):
        print("NAME",qc.data[i].operation.name)
        if qc.data[i].operation.name == 'barrier':
            print('in here')
            latex_src_dirac_states.append('$' + barrier_states[current_barrier_state_index]+'$')
            current_barrier_state_index = current_barrier_state_index+1
        else:
            latex_src_dirac_states.append(qc.data[i].operation.name)
    print(latex_src_dirac_states)
    return latex_src_dirac_states


def create_dirac_state_images(qc):
    parent_directory = os.getcwd()
    directory_dirac = "dirac"
    
    path_dirac = os.path.join(parent_directory, directory_dirac)
    if os.path.exists(path_dirac):
        shutil.rmtree(path_dirac)
    os.mkdir(path_dirac) 
    barrier_latex_states = get_barrier_states(qc, 3)
    print(barrier_latex_states)
    latex_src_dirac_states = compile_latex_src_dirac_states(qc, barrier_latex_states)
    
    for i in range(0, len(latex_src_dirac_states)):
        print(latex_src_dirac_states[i])
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, latex_src_dirac_states[i], fontsize=14, ha='center', va='center', transform=ax.transAxes)
        ax.axis('off')
        plt.savefig(path_dirac + '/' + str(i)+'.png', dpi=300, bbox_inches='tight')