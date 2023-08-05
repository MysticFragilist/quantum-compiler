from gates import graph
from services import processor as ProcessorBL
import sys
import os
import pennylane as qml

from services.compilator import Compilator
from services.transpiler import Transpiler

input_file = sys.argv[-1]
# Process input file
processor = ProcessorBL.SemanticAnalyser()
processor.apply_gates(input_file)

# Build the graph and show it
in_graph = graph.Graph(processor.gates, processor.qubits)
in_graph.draw_graph("Input Graph")

# Compile the graph into a smaller form
compilator = Compilator(in_graph)
compilator.compile()

print([str(item) for item in in_graph.nodes])

#process the output compiled into a new processor to generate a smaller end circuit
processorInt = ProcessorBL.SemanticAnalyser()
# init the circuit manually since we will add gates manually
processorInt.init_circuit(processor.qubits, processor.cbits)

for node in in_graph.nodes:
    processorInt.apply_gate(node.gate.name, node.wire)

# transpile the output processor into a new OUTPUT file
out_file = os.path.basename(input_file)
transpiler = Transpiler(out_file, processorInt.gates)
transpiler.build_file(processorInt.qubits, processorInt.cbits)

# Process the new output file and build the new graph
processorOut = ProcessorBL.SemanticAnalyser()
processorOut.apply_gates(transpiler.output_file)
out_graph = graph.Graph(processorOut.gates, processorOut.qubits)
out_graph.draw_graph("Output Graph")
