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
from model.general_utils import *

BASE_HEIGHT = 100

# Circuit functions

def add_barriers(qc):
    if qc.data[len(qc.data)-1].operation.name != 'barrier':
        qc.barrier()
    barrier = qc.data[len(qc.data)-1]
    
    new_data = []
    for i in range(0, len(qc.data)):
        if i > 0 and qc.data[i].operation.name != 'barrier':
            barrier_to_append = barrier.copy()
            new_data.append(barrier_to_append)

        new_gate = qc.data[i].copy()
        new_data.append(new_gate)
    qc.data = new_data
    
    return qc

def create_circuit_barrier_images(num_bits):
    parent_directory = os.getcwd()
    directory_circ_barriers = "circ_barriers"
    path_circ_barriers = os.path.join(parent_directory, directory_circ_barriers)
    if os.path.exists(path_circ_barriers):
        shutil.rmtree(path_circ_barriers)
    os.mkdir(path_circ_barriers) 

    qc = QuantumCircuit(num_bits)
    qc.barrier()

    buf_not_selected = BytesIO()
    buf_selected = BytesIO()

    qc.draw('mpl').savefig(buf_not_selected, bbox_inches="tight")
    qc.draw('mpl', style=STYLE_SETTINGS).savefig(buf_selected, bbox_inches="tight")
    
    not_selected_image = crop_image(Image.open(buf_not_selected))
    selected_image = crop_image(Image.open(buf_selected))

    not_selected_image.save(path_circ_barriers + '/' + 'not_selected.png')
    selected_image.save(path_circ_barriers + '/' + 'selected.png')

    
def gates_to_figures(qc, directory):

    num_qubits = qc.data[-1].operation.num_qubits
    
    for i in range(0, len(qc.data)):

        if i%2!=0:
            continue

        path = os.path.join(directory, str(i))
        os.mkdir(path) 
        qc_gate_not_selected = QuantumCircuit(num_qubits)
        qc_gate_selected = QuantumCircuit(num_qubits)

        qc_gate_not_selected.data.append(qc.data[i].copy())
        qc_gate_selected.data.append(qc.data[i].copy())
        buf_not_selected = BytesIO()
        buf_selected = BytesIO()
        
        qc_gate_not_selected.draw('mpl').savefig(buf_not_selected, bbox_inches="tight")
        qc_gate_selected.draw('mpl', style=STYLE_SETTINGS).savefig(buf_selected, bbox_inches="tight")
        
        not_selected_image = crop_image(Image.open(buf_not_selected), right_crop_only=(i == 0 if True else False))
        selected_image = crop_image(Image.open(buf_selected), right_crop_only=(i == 0 if True else False))

        not_selected_image.save(path + '/' + 'not_selected.png')
        selected_image.save(path + '/' + 'selected.png')    
        
def create_highlighted_circuit_figures(qc: QuantumCircuit):

    parent_directory = os.getcwd()
    directory_circ = "circ"
    path_circ = os.path.join(parent_directory, directory_circ)
    if os.path.exists(path_circ):
        shutil.rmtree(path_circ)
    os.mkdir(path_circ) 
    
    qc = qc.copy()
    qc = add_barriers(qc)

    gates_to_figures(qc, path_circ)

    return qc