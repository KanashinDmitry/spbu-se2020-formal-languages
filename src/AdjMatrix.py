from pygraphblas import Matrix, BOOL, semiring
from typing import Dict, Tuple, List
from src.Graph import Graph


class AdjMatrix:
    def __init__(self, graph):
        self.M_dict: Dict[str, Tuple[List[int], List[int]]] = {}
        self.M_bin: Dict[str, Matrix] = {}
        self.graph: Graph = graph
        self.graph_to_bin_matrix()

    def graph_to_bin_matrix(self):
        graph = self.graph
        edges = graph.edges

        for v_from, key, v_to in edges:
            if key in self.M_dict:
                self.M_dict[key][0].append(int(v_from))
                self.M_dict[key][1].append(int(v_to))
            else:
                self.M_dict[key] = ([int(v_from)], [int(v_to)])

        for key, nodes in self.M_dict.items():
            num_edges = len(nodes[0])
            self.M_bin[key] = Matrix.from_lists(nodes[0], nodes[1], [True] * num_edges
                                                , nrows = graph.vertices_num, ncols = graph.vertices_num)

    @classmethod
    def adj_kronecker(cls, left: Dict[str, Matrix], right: Dict[str, Matrix]):
        res: Dict[str, Matrix] = {}

        for word in left.keys():
            if word in right.keys():
                res[word] = left[word].kronecker(right[word])

        return res

    @classmethod
    def merge_label_matrices(cls, matrices: Dict[str, Matrix], num_vertices):
        result_matrix = Matrix.sparse(BOOL, num_vertices, num_vertices)
        
        with semiring.LOR_LAND_BOOL:
            for _, matrix in matrices.items(): 
                result_matrix += matrix

        return result_matrix

    @classmethod
    def reachable_vertices(cls, matrix: Matrix):
        res = []

        for row, col in zip(matrix.rows, matrix.cols):
            res.append((row, col))
        
        return res

    @classmethod
    def transitive_closure(cls, matrix: Matrix):
        old_non_zero_elems = -1
        new_non_zero_elems = matrix.nvals

        while(old_non_zero_elems != matrix.nvals):
            matrix += matrix @ matrix
            
            old_non_zero_elems = new_non_zero_elems
            new_non_zero_elems = matrix.nvals

        return matrix
