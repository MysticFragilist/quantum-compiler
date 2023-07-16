class NodeGate:
    def __init__(self, gate_name, gate, wire) -> None:
        self.name = gate_name
        self.wire = wire
        self.gate = gate
        self.children = []

    def add_child(self, node) -> None:
        isNode = isinstance(node, self.__class__)
        
        if not isNode:
            raise TypeError(f"Expected {self.__class__}, got {type(node)}")
        
        self.children.append(node)

    def __str__(self) -> str:
        return f"{self.name}({self.wire})"

    def __eq__(self, other):
        isNode = isinstance(other, self.__class__)
        if not isNode:
            return False
        
        if self.name != other.name:
            return False
        
        return True