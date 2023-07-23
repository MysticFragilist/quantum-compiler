import os


class Transpiler:
    
    def __init__(self, file_name, gates: list):
        self.out_folder = os.path.join('..', 'out')
        self.gates = gates
        self.file_name = file_name

    def build_file(self, qubit_nb: int, bits_nb: int):
        self.output_file = os.path.join(self.out_folder, self.file_name)
        f = open(self.output_file, "w+")
        f.write(f"{qubit_nb},{bits_nb}\n")
        f.write("# this file was compiled using the mini-pcoast compiler.\n")
        f.write("# the content was auto generated to reduce gates depth.\n")
        
        for gate in self.gates:
            if isinstance(gate.wire, list):
                f.write(f"{gate.name}({gate.wire[0]}, {gate.wire[1]})\n")
            elif isinstance(gate.wire, int):
                f.write(f"{gate.name}({gate.wire})\n")
            f.write(f"{gate.name}({gate.wire})\n")
        
        f.close()
