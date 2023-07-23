from gates import graph
from services import processor as ProcessorBL
import sys
import os
import pennylane as qml

from services.compilator import Compilator
from services.transpiler import Transpiler

input_file = sys.argv[-1]
# Process input file
processor = ProcessorBL.Processor()
processor.apply_gates(input_file)

# Build the graph and show it
in_graph = graph.Graph(processor.gates, processor.qubits)
in_graph.draw_graph("Input Graph")

# Compile the graph into a smaller form
compilator = Compilator(in_graph)
compilator.compile()

#process the output compiled into a new processor to generate a smaller end circuit
processorOut = ProcessorBL.Processor()
# init the circuit manually since we will add gates manually
processorOut.init_circuit(processor.qubits, processor.cbits)

for node in in_graph.nodes:
    processorOut.apply_gate(node.gate.name, node.wire)

# transpile the output processor into a new OUTPUT file
out_file = os.path.basename(input_file)
transpiler = Transpiler(out_file, processorOut.gates)
transpiler.build_file(processor.qubits, processor.cbits)

# Process the new output file and build the new graph  
processorOut = ProcessorBL.Processor()
processorOut.apply_gates(transpiler.output_file)
out_graph = graph.Graph(processorOut.gates, processorOut.qubits)
out_graph.draw_graph("Output Graph")