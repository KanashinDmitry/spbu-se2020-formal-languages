from pyformlang.finite_automaton import NondeterministicFiniteAutomaton, State, Symbol
from pyformlang.cfg import CFG, Terminal, Variable, Epsilon
from src.CFGrammar import CFGrammar
from typing import List, Tuple


class Graph:
    def __init__(self, edges):
        self.edges: List[Tuple[int, str, int]] = edges
        self.vertices = set()
        for v_from, _, v_to in self.edges:
            self.vertices.add(v_from)
            self.vertices.add(v_to)
        self.vertices_num = len(self.vertices)

    def cfpq(self, cfg: CFGrammar):
        query = cfg.cfg
        edges = self.edges
        reachable_pairs = set()

        # adding buckles
        for v, terminal, u in edges:
            for production in query.productions:
                if v == u and production.body == []:
                    reachable_pairs.add((production.head, v, v))

        query = cfg.cnf

        for v, terminal, u in edges:
            for production in query.productions:
                if production.body == [Terminal(terminal)]:
                    reachable_pairs.add((production.head, v, u))

        working_set = reachable_pairs.copy()

        while len(working_set) != 0:
            variable, v_from, v_to = working_set.pop()

            new_pairs = set()

            for variable_left, left_v_from, v_new in reachable_pairs:
                if v_new == v_from:
                    for production in query.productions:
                        if not (production.head, left_v_from, v_to) in reachable_pairs \
                           and len(production.body) == 2 \
                           and variable_left == production.body[0] \
                           and variable == production.body[1]:
                            new_pairs.add((production.head, left_v_from, v_to))

            for variable_right, v_new, right_v_to in reachable_pairs:
                if v_new == v_to:
                    for production in query.productions:
                        if not (production.head, v_from, right_v_to) in reachable_pairs \
                           and len(production.body) == 2 \
                           and variable == production.body[0] \
                           and variable_right == production.body[1]:
                            new_pairs.add((production.head, v_from, right_v_to))

            working_set |= new_pairs
            reachable_pairs |= new_pairs

        result = [(v_from, v_to) for variable, v_from, v_to in reachable_pairs
                                 if variable == query.start_symbol]

        return result

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
