from qiskit import QuantumCircuit, QuantumRegister
from qiskit.quantum_info import Statevector
from io import BytesIO
from binascii import b2a_base64
from PIL import Image
import os
import shutil
from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Tahoma']
import matplotlib.pyplot as plt

import numpy as np
import sympy
from model.general_utils import *

CONTROLLED_PHASE = 'cp'
CONTROLLED_Z_ROTATION = 'crz'
CONTROLLED_U_GATE = 'cu'
LIST_Of_GATES_WITH_THETA_PARAM = ['cp', 'crx', 'cry', 'crz', 'cu', 'mcrx', 'mcry', 'ms', 'p', 'r', 'rx','rxx',
                                  'ry', 'ryy', 'rzx', 'rzz', 'u']

def get_barrier_states(qc, num_qubits):
    states = []

    qc_rev = qc.reverse_bits()

    for i in range(0, len(qc_rev.data)):
        temp_circuit = QuantumCircuit(num_qubits)
        new_data = []
        for j in range(0, i):
            new_data.append(qc_rev.data[j])
        temp_circuit.data = new_data
        states.append(Statevector(temp_circuit).reverse_qargs().draw(output='latex_source'))

    states.append(Statevector(qc_rev).draw(output='latex_source'))
    return states

#TODO combine this with create_dirac_state_images()
def compile_latex_src_dirac_states(qc, barrier_states):
    latex_src_dirac_states = []
    current_barrier_state_index = 1
    latex_src_dirac_states.append('$' + barrier_states[0]+'$')
    for i in range(0, len(qc)):

        if qc.data[i].operation.name == 'barrier':
            latex_src_dirac_states.append('$' + barrier_states[current_barrier_state_index]+'$')
            current_barrier_state_index = current_barrier_state_index+1

        else:
            name = qc.data[i].operation.name
            if name == CONTROLLED_PHASE:
                latex_src_dirac_states.append(add_identity_matrices_to_latex_gate(format_name_with_angle_value(name, qc.data[i].operation.params[0]), get_index_list_from_qubits(qc.data[i].qubits), qc.num_qubits, dirac=True))
            else:
                latex_src_dirac_states.append(add_identity_matrices_to_latex_gate(name, get_index_list_from_qubits(qc.data[i].qubits), qc.num_qubits, dirac=True))

    return latex_src_dirac_states


def create_dirac_state_images(qc_orig, qc_barriers):
    parent_directory = os.getcwd()
    directory_dirac = "dirac"
    
    path_dirac = os.path.join(parent_directory, directory_dirac)
    if os.path.exists(path_dirac):
        shutil.rmtree(path_dirac)
    os.mkdir(path_dirac) 

    barrier_latex_states = get_barrier_states(qc_orig, (len(qc_barriers.data[-1].qubits)+len(qc_barriers.data[-1].clbits)))
    latex_src_dirac_states = compile_latex_src_dirac_states(qc_barriers, barrier_latex_states)
    
    for i in range(0, len(latex_src_dirac_states)):
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, latex_src_dirac_states[i], fontsize=80, ha='center', va='center', transform=ax.transAxes, color=SELECTED_COLOUR)
        ax.axis('off')
        plt.savefig(path_dirac + '/' + str(i)+'.svg', dpi=300, bbox_inches='tight')
        plt.close()

def create_dirac_equation_images(qc):

    parent_directory = os.getcwd()
    directory_dirac = "dirac_equations"
    
    path_dirac = os.path.join(parent_directory, directory_dirac)
    if os.path.exists(path_dirac):
        shutil.rmtree(path_dirac)
    os.mkdir(path_dirac) 
    data = qc.data

    init_gates = number_of_init_gates(qc)

    for i in range(init_gates, len(data)):
        # TODO rename... refactor...
        instance_path = os.path.join(path_dirac, str(i))
        os.mkdir(instance_path) 

        # For states
        if data[i].operation.name == 'barrier':
            fig, ax = plt.subplots()
            ax.text(0.5, 0.5, '$ ? $', fontsize=80, ha='center', va='center', transform=ax.transAxes)
            ax.axis('off')
            plt.savefig(instance_path + '/not_selected.svg', dpi=300)
            plt.close()

            fig, ax = plt.subplots()
            ax.text(0.5, 0.5, '$ ? $', fontsize=80, ha='center', va='center', fontfamily='helvetica', transform=ax.transAxes, color=SELECTED_COLOUR)
            ax.axis('off')
            plt.savefig(instance_path + '/selected.svg', dpi=300)
            plt.close()

        # For gates
        else:

            # Add identity matrices
            name = data[i].operation.name
            gate_formatted_latex_src = None

            #TODO account for phi and lambda params as well
            if name in LIST_Of_GATES_WITH_THETA_PARAM:
                gate_formatted_latex_src = add_identity_matrices_to_latex_gate(format_name_with_angle_value(name, qc.data[i].operation.params[0]), get_index_list_from_qubits(data[i].qubits), qc.num_qubits, dirac=True)
            else:
                gate_formatted_latex_src = add_identity_matrices_to_latex_gate(name, get_index_list_from_qubits(data[i].qubits), qc.num_qubits, dirac=True)
            fig, ax = plt.subplots()
            ax.text(0.5, 0.5, gate_formatted_latex_src, fontsize=80, ha='center', va='center', fontfamily='helvetica', transform=ax.transAxes)
            ax.axis('off')
            plt.savefig(instance_path + '/not_selected.svg', dpi=300, bbox_inches='tight')
            plt.close()

            fig, ax = plt.subplots()
            ax.text(0.5, 0.5, gate_formatted_latex_src, fontsize=80, ha='center', va='center', transform=ax.transAxes, color=SELECTED_COLOUR)
            ax.axis('off')
            plt.savefig(instance_path + '/selected.svg', dpi=300, bbox_inches='tight')
            plt.close()
    # Generate images


