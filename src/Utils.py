from pyformlang.finite_automaton import EpsilonNFA
from pyformlang.regular_expression import Regex
import os


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


def read_tokens(name):
    tokens = dict()

    with open(name, 'r') as file:
        for line in file.readlines():
            line_n = line.rstrip().split(" ")
            #print(line_n)
            token, _, word = line_n
            tokens[word] = token

    return tokens


def read_grammar_with_tokens(name_g, name_t):
    tokens = read_tokens(name_t)

    with open(name_g, 'r') as file:
        for line in file.readlines():
            line_n = line.rstrip().split(" ")
            print(line_n)
            head, _, *body = line_n
            tokens[token] = word

    return 0
