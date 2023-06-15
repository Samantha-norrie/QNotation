from qiskit import QuantumCircuit
from qnotation import QNotation

def make_qc():
    qc = QuantumCircuit(3)
    qc.h(0)
    qc.h(1)
    qc.h(0)
    qc.h(2)
    qc.x(1)

    return qc

QNotation.view_notations(make_qc())

