from pyformlang.finite_automaton import EpsilonNFA, DeterministicFiniteAutomaton, State, Symbol
from pyformlang.regular_expression import Regex
from pygraphblas import Matrix, BOOL  
from typing import Dict, Tuple, List
from src.Graph import Graph
from src.AdjMatrix import AdjMatrix


class Automaton:
    def __init__(self, dfa=None):
        self.start_states = []
        self.final_states = []
        self.dfa = dfa
        if dfa is not None: 
            self.graph: Graph = self.dfa_to_graph()
            self.adj_matrices = AdjMatrix(self.graph).M_bin
            self.full_matrix = AdjMatrix.merge_label_matrices(self.adj_matrices, self.graph.vertices_num)

    def to_automaton(self):
        nfa = EpsilonNFA()
        matrices = self.adj_matrices

        for start_state in self.start_states:
            nfa.add_start_state(State(start_state))

        for final_state in self.final_states:
            nfa.add_final_state(State(final_state))

        for word in matrices.keys():
            matrix = matrices[word]
            symb = Symbol(word)

            for row, col in zip(matrix.rows, matrix.cols):
                nfa.add_transition(State(row), symb, State(col))

        return nfa


    def dfa_to_graph(self):
        dfa = self.dfa
        edges = []
        
        states = dict([(state, index) for index, state in enumerate(dfa.states)])
        
        self.start_states = [states[state] for state in dfa.start_states]
        self.final_states = [states[state] for state in dfa.final_states]

        for v_from, transitions in dfa.to_dict().items():
            for value, v_to in transitions.items():     
                edges.append((states[v_from], value, states[v_to]))
        
        return Graph(edges)

    def get_intersection(self, other):        
        adj_graph_automaton = self.adj_matrices
        adj_query_automaton = other.adj_matrices

        num_vertices_graph = self.graph.vertices_num
        num_vertices_query = other.graph.vertices_num

        num_vertices_intersection = num_vertices_graph *  num_vertices_query 

        adj_intersection = AdjMatrix.adj_kronecker(adj_graph_automaton, adj_query_automaton)

        start_states = []
        final_states = []

        for start_state in other.start_states:
            start_states += [start_state + i * num_vertices_query for i in range(num_vertices_graph)]

        for final_state in other.final_states:
            final_states += [final_state + i * num_vertices_query for i in range(num_vertices_graph)]

        result_matrix = AdjMatrix.merge_label_matrices(adj_intersection, num_vertices_intersection)
        
        trans_closure = AdjMatrix.transitive_closure(result_matrix)

        result_automaton = Automaton()
        result_automaton.adj_matrices = adj_intersection
        result_automaton.start_states = start_states
        result_automaton.final_states = final_states
        result_automaton.full_matrix = trans_closure
 
        return result_automaton

    def reach(self, other):
        start_x_final = []

        intersection = self.get_intersection(other)

        start_states = intersection.start_states
        final_states = intersection.final_states

        matrix_intersection = intersection.full_matrix
        
        reachable_vertices = AdjMatrix.reachable_vertices(matrix_intersection)

        for v_from, v_to in reachable_vertices:
            if v_from in start_states and v_to in final_states:
                start_x_final.append((v_from // other.graph.vertices_num, v_to // other.graph.vertices_num))

        return start_x_final        

    def reach_all(self, other):
        start_x_final = self.reach(other)
        
        for v_from, v_to in start_x_final:
            print(f'{v_from} {v_to}')

        return start_x_final


    def reach_from(self, other, given_started):
        start_x_final = self.reach(other)
        res = []
        
        for v_from, v_to in start_x_final:
            if v_from in given_started:
                res.append((v_from, v_to))
                print(f'{v_from} {v_to}')

        return res

    def reach_from_to(self, other, given_started, given_final):
        start_x_final = self.reach(other)
        res = []
        
        for v_from, v_to in start_x_final:
            if v_from in given_started and v_to in given_final:
                res.append((v_from, v_to))
                print(f'{v_from} {v_to}')

        return res


    @classmethod
    def from_graph(cls, graph):
        automat = Automaton()
        automat.start_states = list(graph.vertices)
        automat.final_states = list(graph.vertices)
        automat.graph = graph
        automat.adj_matrices = AdjMatrix(graph).M_bin
        automat.full_matrix = AdjMatrix.merge_label_matrices(automat.adj_matrices, automat.graph.vertices_num)

        return automat
