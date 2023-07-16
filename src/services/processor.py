import pennylane as qml
from gates import graph

class Processor:
    def __init__(self, qubits: int, cbits: int):
        self.qubits = qubits
        self.cbits = cbits
        self.device = qml.device('default.qubit', wires=qubits)
        self.pennylane_gates = []
        self.gates = []
        
    def apply_gate(self, gate, qubits: list | int):
        # Fetch the class type with the provided gate string name
        qml_type = getattr(qml, gate)(qubits)
        self.pennylane_gates.append(qml_type)
        self.gates.append(graph.NodeGate(gate, qml_type, qubits))

    def build_circuit(self):
        # Create a quantum circuit and apply the gates
        @qml.qnode(self.device)
        def circuit():
            for gate in self.pennylane_gates:
                gate
            return qml.probs(wires=range(self.qubits))
        return circuit()