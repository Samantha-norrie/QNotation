# QNotation

## Introduction
Welcome to QNotation! QNotation is a visual and interactive tool designed to support the learning of circuit, Dirac, and matrix notation
within the context of Quantum Computing. The aforementioned notations are the three main notations used in Quantum Computing. Why is it important to learn
these notations? As stated by Richard Feynman, in order for one to truly comprehend their field and all of its nuances, they must be able
to read and use all of its notations!

## How to Use (Programmer's Version)

### Installing QNotation *(Coming Soon!)*

QNotation is currently still being built! Once the first version of the tool is released, users will be able to use pip to install the tool.

### Using QNotation

## How to Use (Absolute Beginner's Version)

If you have never written a line of code before, this section is for you!

### Installing Python

Python can be downloaded from [python.org](https://www.python.org). Make sure to download a version of Python that is 3.X.X.

### Installing Jupyter Notebook

I recommend installing Jupyter Notebook through [Anaconda](https://www.anaconda.com/download).Anaconda includes Jupyter Notebook and many other cool
tools for Python. [Here is a great tutorial on how to use Jupyter Notebook](https://www.codecademy.com/article/how-to-use-jupyter-notebooks).

### Installing Qiskit

Qiskit is one of the most popular Quantum Computing libraries! [This tutorial explains how to download it](https://qiskit.org/documentation/getting_started.html).
The tutorial assumes that the user has pip installed. Pip can be installed by following [these instructions](https://pip.pypa.io/en/stable/installation/).

### Installing QNotation *(Coming Soon!)*

QNotation is currently still being built! Once the first version of the tool is released, users will be able to use pip to download the tool.

### Creating Your First Quantum Circuit for QNotation

```python
# Step 1: Import the required packages
from qiskit import QuantumCircuit
from qnotation import QNotation

# Step 2: Create your QuantumCircuit object (https://qiskit.org/documentation/apidoc/circuit.html)
qc = QuantumCircuit(3)
qc.h(0)
qc.x(1)

# Step 3: Run QNotation
QNotation.view\_notations(qc)
```
