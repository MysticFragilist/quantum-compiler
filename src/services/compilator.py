from gates.graph import Graph
from operations.duplicate_own_commute import DuplicateOwnCommuteGate
from operations.pauli_group_reduction import PauliGroupReduction

class Compilator:
    def __init__(self, graph):
        self.graph = graph
        self.operations = [
            DuplicateOwnCommuteGate(self.graph),
            PauliGroupReduction(self.graph)
        ]

    def compile(self):
        """Compiles the operations list into a quantum circuit."""
        for operation in self.operations:
            operation.apply()
        print("Compilation done.")

        pass