from pyformlang.finite_automaton import NondeterministicFiniteAutomaton, State, Symbol
from typing import List, Tuple


class Graph:
    def __init__(self, edges):
        self.edges: List[Tuple[int, str, int]] = edges
        self.vertices = set()
        for v_from, _, v_to in self.edges:
           self.vertices.add(v_from)
           self.vertices.add(v_to)
        self.vertices_num = len(self.vertices)

    @classmethod
    def graph_to_nfa(cls, start_states, final_states, transitions: List[Tuple[int, str, int]]):
        nfa = NondeterministicFiniteAutomaton()

        for start_state in start_states:
            nfa.add_start_state(State(start_state))

        for final_state in final_states:
            nfa.add_final_state(State(final_state))

        for st_from, label, st_to in transitions:
            nfa.add_transition(State(st_from), Symbol(label), State(st_to))
        
        return nfa
