import pennylane as qml

class Processor:
    def __init__(self, qubits: int, cbits: int):
        self.qubits = qubits
        self.cbits = cbits
        self.device = qml.device('default.qubit', wires=qubits)
        self.operators = []
        
    def apply_gate(self, gate, qubits: list | int):
        # Fetch the class type with the provided gate string name
        #
        # Example:
        #   gate = "Hadamard"
        #   qml_type = type(qml.Hadamard)
        # Where qml is a module
        qml_type = getattr(qml, gate)(qubits)
        self.operators.append(qml_type)
        print(qml_type)

    def build_circuit(self):
        # Create a quantum circuit and apply the gates
        @qml.qnode(self.device)
        def circuit():
            for operator in self.operators:
                operator
            return qml.probs(wires=range(self.qubits))
        return circuit()