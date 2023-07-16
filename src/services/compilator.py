from gates.graph import Graph
from operations.lemma1 import Lemma1

class Compilator:
    def __init__(self, gates):
        self.gates = gates
        self.graph = Graph(self.gates)
        self.operations = [
            Lemma1(self.graph)
        ]

    def compile(self):
        """Compiles the operations list into a quantum circuit."""
        for operation in self.operations:
            operation.apply()

        pass