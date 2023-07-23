from gates.graph import Graph
from operations.duplicate import Duplicate
from operations.lemma1 import Lemma1

class Compilator:
    def __init__(self, graph):
        self.graph = graph
        self.operations = [
            Duplicate(self.graph),
            Lemma1(self.graph)
        ]

    def compile(self):
        """Compiles the operations list into a quantum circuit."""
        for operation in self.operations:
            operation.apply()

        pass