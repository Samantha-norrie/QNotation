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

BASE_HEIGHT = 100

# Circuit functions

def add_barriers(qc):
    if qc.data[len(qc.data)-1].operation.name != 'barrier':
        qc.barrier()
    barrier = qc.data[len(qc.data)-1]
    
    new_data = []
    for i in range(0, len(qc.data)):
        if qc.data[i].operation.name != 'barrier':
            barrier_to_append = barrier.copy()
            new_data.append(barrier_to_append)

        new_gate = qc.data[i].copy()
        new_data.append(new_gate)
    qc.data = new_data
    
    return qc

def format_figure(mpl_obj, crop=True):
    img_bio = BytesIO()
    mpl_obj.savefig(img_bio, format="png", bbox_inches="tight")
    mpl_obj.clf()

    img_data = b2a_base64(img_bio.getvalue()).decode()
    img_html = f"""
        <div class="circuit-plot-wpr">
            <img src="data:image/png;base64,{img_data}&#10;">
        </div>
        """
    return img_html

def crop_image(image, right_crop_only=False):
    width, height = image.size
    if right_crop_only:
        return image.crop((0, 0, width-12, height))
    return image.crop((90, 0, width-12, height))
    
def gates_to_figures(qc, directory):
    images = []
    # Can be done as first gate will always be a barrier
    num_qubits = qc.data[0].operation.num_qubits
    
    # TODO fix regex
    style_settings = {'displaycolor': {'x': ('#c12f98', '#FFFFFF')},
                      'gatefacecolor': '#f05400',
                    'barrierfacecolor': '#f05400'}
    for i in range(0, len(qc.data)):
        image_pair = []
        path = os.path.join(directory, str(i))
        os.mkdir(path) 
        qc_gate_not_selected = QuantumCircuit(num_qubits)
        qc_gate_selected = QuantumCircuit(num_qubits)
        
        qc_gate_not_selected.data.append(qc.data[i].copy())
        qc_gate_selected.data.append(qc.data[i].copy())
        buf_not_selected = BytesIO()
        buf_selected = BytesIO()
        
        qc_gate_not_selected.draw('mpl').savefig(buf_not_selected, bbox_inches="tight")
        qc_gate_selected.draw('mpl', style=style_settings).savefig(buf_selected, bbox_inches="tight")
        
        not_selected_image = crop_image(Image.open(buf_not_selected), right_crop_only=(i == 0 if True else False))
        selected_image = crop_image(Image.open(buf_selected), right_crop_only=(i == 0 if True else False))

        hpercent = (BASE_HEIGHT/float(selected_image.size[1]))
        wsize = int((float(selected_image.size[0])*float(hpercent)))

        # not_selected_image.resize((wsize, BASE_HEIGHT))
        # selected_image.resize((wsize, BASE_HEIGHT))

        not_selected_image.save(path + '/' + 'not_selected.png')
        selected_image.save(path + '/' + 'selected.png')
        
    
    return images       
        
def create_highlighted_circuit_figures(qc: QuantumCircuit):

    parent_directory = os.getcwd()
    directory_circ = "circ"
    path_circ = os.path.join(parent_directory, directory_circ)
    if os.path.exists(path_circ):
        shutil.rmtree(path_circ)
    os.mkdir(path_circ) 
    
    qc = qc.copy()
    qc = add_barriers(qc)
    separated_figures = []

    gates_to_figures(qc, path_circ)

    return qc