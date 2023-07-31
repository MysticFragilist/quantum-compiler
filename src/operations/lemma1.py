from gates.node_gate import NodeGate
from operations.operation import Operation
import pennylane as qml

class Lemma1(Operation):    
    def apply(self):
        """Applies Lemma 1 to the graph."""
        print("Applying Lemma 1")

        # Find patterns
        self._navigate_breadth_first(self.gates_graph.root, [])


    def _navigate_breadth_first(self, node, saved_nodes):
        saved_nodes = saved_nodes[:]
        print([str(item) for item in saved_nodes])
        if len(saved_nodes) == 4:
            p_1 = saved_nodes[0].gate
            p_2 = saved_nodes[1].gate
            exponent = self._lambda_function(p_1, p_2)
            new_gate = (-1) ** exponent * qml.Identity(saved_nodes[0].wire)
            
            new_node = NodeGate("Identity", new_gate.name, new_gate.wire)

            before_pattern_match_first_node = saved_nodes[0].parent
            before_pattern_match_first_node.children.remove(saved_nodes[0])
            before_pattern_match_first_node.add_child(new_node)
            new_node.children = saved_nodes[-1].children

            for child in new_node.children:
                child.parent = new_node

        if not node.gate or not self._is_clifford(node.gate):
            pass

        saved_nodes.append(node)
        for child in node.children:
            if child.name != node.name and len(saved_nodes) > 1:
                print(child.name, saved_nodes[-2].name)
                if child.name == saved_nodes[-2].name:
                    saved_nodes.append(child)
                    self._navigate_breadth_first(child, saved_nodes)
                    continue
            elif child.name != node.name and len(saved_nodes) == 1:
                saved_nodes.append(child)
                self._navigate_breadth_first(child, saved_nodes)
                continue
            saved_nodes = []
            self._navigate_breadth_first(child, saved_nodes)


    def _is_clifford(self, gate) -> bool:
        if gate.name == "Hadamard" or gate.name == "H":
            return True
        if "Pauli" in gate.name:
            return True
        
        return False
        

    def _lambda_function(self, gate_p1, gate_p2):
        if qml.is_commuting(gate_p1, gate_p2):
            return 0
        else:
            return 1