from qiskit import QuantumCircuit, QuantumRegister
from qiskit.quantum_info import Statevector
from io import BytesIO
from binascii import b2a_base64
from PIL import Image
import os
import shutil
import matplotlib.pyplot as plt

import numpy as np
import sympy
from model.general_utils import *

def get_barrier_states(qc, num_qubits):
    states = []

    for i in range(0, len(qc.data)):
        temp_circuit = QuantumCircuit(num_qubits)
        new_data = []
        for j in range(0, i):
            new_data.append(qc.data[j])
        temp_circuit.data = new_data
        states.append(Statevector(temp_circuit).draw(output='latex_source'))

    states.append(Statevector(qc).draw(output='latex_source'))
    return states

def compile_latex_src_dirac_states(qc, barrier_states):
    latex_src_dirac_states = []
    current_barrier_state_index = 0

    for i in range(0, len(qc)):

        if qc.data[i].operation.name == 'barrier':
            latex_src_dirac_states.append('$' + barrier_states[current_barrier_state_index]+'$')
            current_barrier_state_index = current_barrier_state_index+1

        else:
            latex_src_dirac_states.append(qc.data[i].operation.name)
    return latex_src_dirac_states


def create_dirac_state_images(qc_orig, qc_barriers):
    parent_directory = os.getcwd()
    directory_dirac = "dirac"
    
    path_dirac = os.path.join(parent_directory, directory_dirac)
    if os.path.exists(path_dirac):
        shutil.rmtree(path_dirac)
    os.mkdir(path_dirac) 
    barrier_latex_states = get_barrier_states(qc_orig, 3)
    latex_src_dirac_states = compile_latex_src_dirac_states(qc_barriers, barrier_latex_states)
    
    for i in range(0, len(latex_src_dirac_states)):
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, latex_src_dirac_states[i], fontsize=80, ha='center', va='center', transform=ax.transAxes)
        ax.axis('off')
        plt.savefig(path_dirac + '/' + str(i)+'.png', dpi=300, bbox_inches='tight')
        plt.close()

def create_dirac_equation_images(qc):

    parent_directory = os.getcwd()
    directory_dirac = "dirac_equations"
    
    path_dirac = os.path.join(parent_directory, directory_dirac)
    if os.path.exists(path_dirac):
        shutil.rmtree(path_dirac)
    os.mkdir(path_dirac) 
    data = qc.data

    for i in range(0, len(data)):
        # TODO rename... refactor...
        instance_path = os.path.join(path_dirac, str(i))
        os.mkdir(instance_path) 

        # For states
        if data[i].operation.name == 'barrier':
            fig, ax = plt.subplots()
            ax.text(0.5, 0.5, '$ ? $', fontsize=80, ha='center', va='center', transform=ax.transAxes)
            ax.axis('off')
            plt.savefig(instance_path + '/not_selected.png', dpi=300, bbox_inches='tight')
            plt.close()

            fig, ax = plt.subplots()
            ax.text(0.5, 0.5, '$ ? $', fontsize=80, ha='center', va='center', transform=ax.transAxes, color='pink')
            ax.axis('off')
            plt.savefig(instance_path + '/selected.png', dpi=300, bbox_inches='tight')
            plt.close()

        # For gates
        else:

            # Add identity matrices
            gate_formatted_latex_src = add_identity_matrices_to_latex_gate(data[i].operation.name, get_index_list_from_qubits(data[i].qubits), qc.num_qubits, dirac=True)

            fig, ax = plt.subplots()
            ax.text(0.5, 0.5, gate_formatted_latex_src, fontsize=80, ha='center', va='center', transform=ax.transAxes)
            ax.axis('off')
            plt.savefig(instance_path + '/not_selected.png', dpi=300, bbox_inches='tight')
            plt.close()

            fig, ax = plt.subplots()
            ax.text(0.5, 0.5, gate_formatted_latex_src, fontsize=80, ha='center', va='center', transform=ax.transAxes, color='pink')
            ax.axis('off')
            plt.savefig(instance_path + '/selected.png', dpi=300, bbox_inches='tight')
            plt.close()
    # Generate images


