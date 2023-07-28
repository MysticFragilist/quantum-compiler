from statistics import mean
from gates.node_gate import NodeGate
import networkx as nx
import matplotlib.pyplot as plt

class Graph:
    def __init__(self, gates, nb_wires):
        self.nodes = []
        self.G = nx.DiGraph(directed=True)
        self.nb_wires = nb_wires
        self.root = NodeGate("root", None, None)
        self.queues = [[] for i in range(nb_wires)]
        self.build_nodes(gates)

    def build_nodes(self, gates):
        for gate in gates:
            if isinstance(gate.wire, list):
                for wire in gate.wire:
                    self.build_node(gate, wire)
                continue
            if isinstance(gate.wire, int):
                self.build_node(gate, gate.wire)
                continue

        self.end = NodeGate("end", None, None)
        for queue in self.queues:
            if len(queue) == 0:
                continue
            node = queue[-1]
            index = len(queue)
            
            self.G.add_edge(str(node), 'end')

    def build_node(self, gate, wire):
        queue = self.queues[wire]
        if len(queue) == 0:
            self.root.add_child(gate)
            gate.height_index = 0
            self.G.add_edge('root', str(gate))
            queue.append(gate)
            self.nodes.append(gate)
            return
        
        index = len(queue)
        last_parent_on_wire = queue.pop()
        last_parent_on_wire.add_child(gate)
        # if the height is already present we are not updating it to prevent hash change
        if gate.height_index == -1:
            gate.height_index = index
            
        self.G.add_edge(str(last_parent_on_wire), str(gate))
        queue.append(last_parent_on_wire)
        queue.append(gate)
        self.nodes.append(gate)

    def build_positions(self):
        node_positions =  {'root': (-1, 1), 'end': (2, 1)}
        max_depth = 0
        for node in self.G.nodes:
            if 'root' in node:
                continue
            if 'end' in node:
                continue
            node_split = node.split('(')
            
            arguments = node_split[1].split('.')
            wire = arguments[0]
            current_depth = int(arguments[1].replace(')', ''))
            max_depth = max(max_depth, current_depth)
            if str(wire).isdigit():
                node_positions[node] = (current_depth, int(wire))
                continue
            else:
                split_wire = wire.replace('[', '').replace(']', '').replace(' ', '').split(',')
                split_wire = [int(i) for i in split_wire]
                node_positions[node] = (current_depth, mean(split_wire))
                continue
        
        node_positions['root'] = (-1, mean([node_positions[i][1] for i in node_positions]))
        node_positions['end'] = (max_depth + 1, mean([node_positions[i][1] for i in node_positions]))
        return node_positions
    
    def draw_graph(self, title="Graph"):
        # print(list(map(lambda x: str(x), list(dict.fromkeys(self.G.nodes)))))
        
        # remove all duplicate nodes from self.G.nodes
        node_positions = self.build_positions()
        # node_positions = nx.spring_layout(self.G)

        # Set the offset for label positions
        label_offset = 0.1

        node_colors = ['black' if node == 'root' or node == 'end' else 'lightblue' for node in self.G.nodes]
        fig = plt.figure(title)

        nx.draw(self.G, node_positions, node_color=node_colors, edgecolors='black', with_labels=False, arrows=True, node_size=150)

        for node, pos in node_positions.items():
            x, y = pos
            plt.text(x, y + label_offset, node, ha='center', va='bottom')
        
        padding = 0.5  # Additional padding around the nodes
        x_values, y_values = zip(*node_positions.values())
        min_x = min(x_values) - padding
        max_x = max(x_values) + padding
        min_y = min(y_values) - padding
        max_y = max(y_values) + padding
        plt.xlim(min_x, max_x)
        plt.ylim(min_y, max_y)

        # Show the plot
        plt.show()