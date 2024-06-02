import numpy as np
import random

class Graph:
    def __init__(self, node=None, saturation=None, graph_type=None):
        self.node = node
        self.saturation = saturation / 100.0 if saturation else None
        self.matrix = np.zeros((node, node), dtype=int) if node else None
        self.graph_type = graph_type
        if graph_type:
            self.generate(graph_type)

    def generate(self, graph_type):
        self.matrix = np.zeros((self.node, self.node), dtype=int)
        if graph_type == "hamilton":
            while True:
                self.generate_edges()
                if self.hamiltonian_cycle():
                    print("Hamiltonian Graph")
                    self.print_graph()
                    break
                self.matrix = np.zeros((self.node, self.node), dtype=int)
        elif graph_type == "non_hamilton":
            while True:
                self.generate_edges()
                if not self.hamiltonian_cycle():
                    print("Non-Hamiltonian Graph")
                    self.print_graph()
                    break
                self.matrix = np.zeros((self.node, self.node), dtype=int)
        else:
            print("Invalid type")

    def generate_edges(self):
        edge_count = int(self.node * (self.node - 1) * self.saturation / 2)
        edges_added = 0
        while edges_added < edge_count:
            i = random.randint(0, self.node - 1)
            j = random.randint(0, self.node - 1)
            if i != j and self.matrix[i][j] == 0:
                self.matrix[i][j] = self.matrix[j][i] = 1
                edges_added += 1

    def hamiltonian_cycle(self):
        path = [-1] * self.node
        path[0] = 0

        if not self.hamiltonian_cycle_util(path, 1):
            return False
        return path + [path[0]]

    def hamiltonian_cycle_util(self, path, pos):
        if pos == self.node:
            return self.matrix[path[pos - 1]][path[0]] == 1

        for v in range(1, self.node):
            if self.is_valid(v, pos, path):
                path[pos] = v

                if self.hamiltonian_cycle_util(path, pos + 1):
                    return True

                path[pos] = -1

        return False

    def is_valid(self, v, pos, path):
        if self.matrix[path[pos - 1]][v] == 0:
            return False

        if v in path:
            return False

        return True

    def print_graph(self):
        print("    " + "  ".join(str(i) for i in range(1, len(self.matrix) + 1)))
        print("--+" + "---" * len(self.matrix))
        for i, row in enumerate(self.matrix, start=1):
            print(f"{i} | {'  '.join(str(cell) for cell in row)}")

    def is_eulerian(self):
        if not self.is_connected():
            return "Graph is not Eulerian"
        else:
            in_out_degree = np.sum(self.matrix, axis=0) - np.sum(self.matrix, axis=1)
            if np.all(in_out_degree == 0):
                return "Graph is Eulerian"
            else:
                return "Graph is not Eulerian"

    def is_connected(self):
        start_vertex = None
        for i in range(self.node):
            if np.sum(self.matrix[i]) > 0:
                start_vertex = i
                break

        if start_vertex is None:
            return True, None

        visited = np.zeros(self.node, dtype=bool)
        path = []
        self.dfs(start_vertex, visited, path)

        for i in range(self.node):
            if np.sum(self.matrix[i]) > 0 and not visited[i]:
                return False
        for i in range(len(path)):
            path[i] += 1
        print("Euler Cycle:", path)
        return True, path

    def dfs(self, v, visited, path):
        visited[v] = True
        path.append(v)

        for i in range(self.node):
            if self.matrix[v][i] == 1 and not visited[i]:
                self.dfs(i, visited, path)



    def draw(self, file):
            with open(file, 'w') as f:
                f.write("\\documentclass{article}\n")
                f.write("\\usepackage{tikz}\n")
                f.write("\\begin{document}\n")
                f.write("\\begin{figure}\n")
                f.write("\\centering\n")
                f.write("\\begin{tikzpicture}[auto, node distance=2cm, every loop/.style={},]\n")
                
                num_nodes = len(self.matrix)

                for node in range(num_nodes):
                    f.write(f"\\node[draw, circle] ({node+1}) at ({(node+1) * 360/num_nodes}:3cm) {{$ {node+1} $}};\n")
                    
                for i in range(num_nodes):
                    for j in range(num_nodes):
                        if self.matrix[i][j] == 1:
                            f.write(f"\\path[-] ({i+1}) edge node {{}} ({j+1});\n")
                
                f.write("\\end{tikzpicture}\n")
                f.write("\\end{figure}\n")
                f.write("\\end{document}\n")
            print(f"Graph exported to {file}")