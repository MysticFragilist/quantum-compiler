from gates import graph
from services import processor as ProcessorBL
import sys

path = sys.argv[-1]

def read_input_file(filename):
    """Reads the input file and returns the list of lines."""
    with open(filename) as file:
        lines = file.readlines()
        header = lines[0].replace('\n', '').split(',')
        return (int(header[0]), int(header[1]), lines[1:])

(qubit_nb, bits_nb, lines) = read_input_file(path)

processor = ProcessorBL.Processor(qubit_nb, bits_nb)

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
        processor.apply_gate(gate_line[0], dissected_qubits[0])
    else:
        processor.apply_gate(gate_line[0], dissected_qubits)


gg = graph.Graph(processor.gates, qubit_nb)

gg.draw_graph()