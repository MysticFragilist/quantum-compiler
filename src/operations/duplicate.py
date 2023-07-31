from operations.operation import Operation


class Duplicate(Operation):
    def apply(self):
        """Remove all duplicate nodes from the graph if the gate is a pi rotation."""
        print("Applying Duplicates")
        self._navigate_breadth_first(self.gates_graph.root)
    
    def _navigate_breadth_first(self, node):
        for child in node.children:
            if child.name == node.name:
                node.children = child.children
                self.gates_graph.nodes.remove(child)
                
                self._navigate_breadth_first(node)
                continue
            self._navigate_breadth_first(child)
