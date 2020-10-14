import os
from src.Graph import Graph
from src.CFGrammar import CFGrammar
from src.Utils import read_graph, parse_pairs
from src.cfpq import cfpq_tensor

DATA_PATH = os.path.join(os.getcwd(), 'tests/data/cfpq')


def test_empty_graph():
    edges = read_graph(os.path.join(DATA_PATH, "graph_empty.txt"))
    graph = Graph(edges)

    cfg = CFGrammar(os.path.join(DATA_PATH, "grammar_1_parentheses.txt"))

    actual = cfpq_tensor(graph, cfg)

    expected = []

    assert expected == actual


def test_1():
    edges = read_graph(os.path.join(DATA_PATH, "graph_1.txt"))
    graph = Graph(edges)

    cfg = CFGrammar(os.path.join(DATA_PATH, "grammar_1_parentheses.txt"))

    actual = set(cfpq_tensor(graph, cfg))

    expected = set(parse_pairs(os.path.join(DATA_PATH, 'res_1.txt')))

    assert expected == actual


# palindrome ww^(-1)
def test_2():
    edges = read_graph(os.path.join(DATA_PATH, "graph_2.txt"))
    graph = Graph(edges)

    cfg = CFGrammar(os.path.join(DATA_PATH, "grammar_2_palindrome.txt"))

    actual = set(cfpq_tensor(graph, cfg))

    expected = set(parse_pairs(os.path.join(DATA_PATH, 'res_2.txt')))

    assert expected == actual


def test_3():
    edges = read_graph(os.path.join(DATA_PATH, "graph_3.txt"))
    graph = Graph(edges)

    cfg = CFGrammar(os.path.join(DATA_PATH, "grammar_3.txt"))

    actual = set(cfpq_tensor(graph, cfg))

    expected = set(parse_pairs(os.path.join(DATA_PATH, 'res_3.txt')))

    assert expected == actual
