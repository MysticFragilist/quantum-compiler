import pennylane as qml
from gates import graph

class Processor:
    def __init__(self):
        self.qubits = 1
        self.cbits = 1
        self.device = qml.device('default.qubit', wires=1)
        self.pennylane_gates = []
        self.gates = []

    def init_circuit(self, qubit_nb: int, bits_nb: int):
        self.qubits = qubit_nb
        self.cbits = bits_nb
        self.device = qml.device('default.qubit', wires=qubit_nb)


    def apply_gates(self, file_name):
        """Applies the gates from the input file."""
        (qubit_nb, bits_nb, lines) = self._read_input_file(file_name)
        # Reinit value after applying header gates
        self.init_circuit(qubit_nb, bits_nb)
        
        # Apply the gates
        for line in lines:
            line = line.replace('\n', '')
            if line == '':
                continue
            if line.find('#') != -1:
                continue
            
            gate_line = line.split('(')
            gate_line[1] = gate_line[1].replace(')', '').split(',')
            dissected_qubits = []
            for i in range(len(gate_line[1])):
                dissected_qubits.append(int(gate_line[1][i]))
            if len(dissected_qubits) == 1:
                self.apply_gate(gate_line[0], dissected_qubits[0])
            else:
                self.apply_gate(gate_line[0], dissected_qubits)


    def _read_input_file(self, filename):
        """Reads the input file and returns the list of lines."""
        with open(filename) as file:
            lines = file.readlines()
            header = lines[0].replace('\n', '').split(',')
            return (int(header[0]), int(header[1]), lines[1:])
    

    def apply_gate(self, gate, qubits: list | int):
        # Fetch the class type with the provided gate string name
        qml_type = getattr(qml, gate)(qubits)
        self.pennylane_gates.append(qml_type)
        self.gates.append(graph.NodeGate(gate, qml_type, qubits))


    def build_circuit(self) -> qml.QNode:
        # Create a quantum circuit and apply the gates
        @qml.qnode(self.device)
        def circuit():
            for gate in self.pennylane_gates:
                gate
            return qml.expval(qml.PauliZ(0))
        qml.draw_mpl(circuit)()
        return circuit()