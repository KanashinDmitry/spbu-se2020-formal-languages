from pyformlang.finite_automaton import EpsilonNFA
from pyformlang.regular_expression import Regex


def regex_to_dfa(regex):
    regex = Regex(regex)

    dfa = regex.to_epsilon_nfa().to_deterministic()

    return dfa


def read_regex(name):
    regex = ""

    with open(name, 'r') as file:
        regex = file.readline()

    return regex


def read_vertices(name):
    vertices = read_regex(name).split(' ')
    
    return vertices


def read_graph(name):
    edges = []

    with open(name, 'r') as file:
        for line in file.readlines():
            v_from, label, v_to = line.rstrip().split(" ")
            edges.append((int(v_from), label, int(v_to)))

    return edges

def parse_pairs(name):
    pairs = []

    with open(name, 'r') as file:
        for line in file.readlines():
            v_from, v_to = line.rstrip().split(" ")
            pairs.append((int(v_from), int(v_to)))
    
    return pairs
