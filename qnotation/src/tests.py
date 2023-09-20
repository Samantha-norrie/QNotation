from qiskit import QuantumCircuit
from qnotation import QNotation
from qiskit.quantum_info import Statevector
import matplotlib.pyplot as plt
plt.rcParams['text.usetex'] = True
def make_qc():
    qc = QuantumCircuit(3)
    qc.h(0)
    qc.h(1)
    qc.h(0)
    qc.h(2)
    qc.x(1)

    return qc

QNotation.view_notations(make_qc())

# txte= Statevector(make_qc()).draw(output='latex_source')

# plt.text(0.0, 0.0, txte, fontsize=14)
# ax = plt.gca()
# ax.axes.get_xaxis().set_visible(False)
# ax.axes.get_yaxis().set_visible(False)

# plt.show()

