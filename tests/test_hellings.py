import os
from src.Graph import Graph
from src.CFGrammar import CFGrammar
from src.Utils import read_graph, parse_pairs

DATA_PATH = os.path.join(os.getcwd(), 'tests/data/hellings')


def test_empty_graph():
    edges = read_graph(os.path.join(DATA_PATH, "graph_empty.txt"))
    graph = Graph(edges)
    
    cfg = CFGrammar(os.path.join(DATA_PATH, "grammar_1_parentheses.txt"))

    actual = graph.cfpq(cfg)

    expected = []
    
    assert expected == actual


def test_parentheses():
    edges = read_graph(os.path.join(DATA_PATH, "graph_1.txt"))
    graph = Graph(edges)
    
    cfg = CFGrammar(os.path.join(DATA_PATH, "grammar_1_parentheses.txt"))

    actual = set(graph.cfpq(cfg))

    expected = set(parse_pairs(os.path.join(DATA_PATH, 'res_1.txt')))
    
    assert expected == actual


# palindrome ww^(-1)
def test_with_buckles():
    edges = read_graph(os.path.join(DATA_PATH, "graph_2.txt"))
    graph = Graph(edges)

    cfg = CFGrammar(os.path.join(DATA_PATH, "grammar_2_palindrome.txt"))

    actual = set(graph.cfpq(cfg))

    expected = set(parse_pairs(os.path.join(DATA_PATH, 'res_2.txt')))
    
    assert expected == actual
