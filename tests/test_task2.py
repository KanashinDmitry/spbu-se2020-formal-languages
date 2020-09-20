import pytest
import os
import sys
import random
from pyformlang.finite_automaton import EpsilonNFA, DeterministicFiniteAutomaton, State, Symbol
from src.Utils import *
from src.Automaton import Automaton
from src.Graph import Graph

DATA_PATH = os.path.join(os.getcwd(), 'tests/data/')


def parse_expected(name):
    res_str = read_graph(name)
    res = list(map(lambda x: (int(x[0]), int(x[1])), res_str))
    
    return res 


def test_query_all():
    edges = read_graph(os.path.join(DATA_PATH, 'graph_all.txt'))
    regex = read_regex(os.path.join(DATA_PATH, 'regex_all.txt'))

    dfa = regex_to_dfa(regex)
    query_automaton = Automaton(dfa)

    graph = Graph(edges)
    automaton_graph = Automaton.from_graph(graph)

    res = automaton_graph.reach_all(query_automaton)

    expected = parse_expected(os.path.join(DATA_PATH, 'res_all.txt'))

    assert expected == res


def test_query_from():
    edges = read_graph(os.path.join(DATA_PATH, 'graph_from.txt'))
    regex = read_regex(os.path.join(DATA_PATH, 'regex_from.txt'))

    dfa = regex_to_dfa(regex)
    query_automaton = Automaton(dfa)

    graph = Graph(edges)
    automaton_graph = Automaton.from_graph(graph)

    res = automaton_graph.reach_from(query_automaton, [0])

    expected = parse_expected(os.path.join(DATA_PATH, 'res_from.txt'))

    assert expected == res


def test_query_from_to():
    edges = read_graph(os.path.join(DATA_PATH, 'graph_from_to.txt'))
    regex = read_regex(os.path.join(DATA_PATH, 'regex_from_to.txt'))

    dfa = regex_to_dfa(regex)
    query_automaton = Automaton(dfa)

    graph = Graph(edges)
    automaton_graph = Automaton.from_graph(graph)

    res = automaton_graph.reach_from_to(query_automaton, [2], [1])

    expected = parse_expected(os.path.join(DATA_PATH, 'res_from_to.txt'))

    assert expected == res


def test_intersection_automata():
    edges = read_graph(os.path.join(DATA_PATH, 'graph_0.txt'))
    regex = read_regex(os.path.join(DATA_PATH, 'regex_0.txt'))

    dfa = regex_to_dfa(regex)
    query_automaton = Automaton(dfa)

    graph = Graph(edges)
    automaton_graph = Automaton.from_graph(graph)

    res = automaton_graph.get_intersection(query_automaton)

    res_automaton = res.to_automaton()

    a = Symbol('a')
    b = Symbol('b')
    c = Symbol('c')

    assert res_automaton.accepts([a, b, c])
    assert res_automaton.accepts([a, c])
    assert res_automaton.accepts([a, c, c])
    assert not res_automaton.accepts([a, b, b, c])
    assert not res_automaton.accepts([a])
    assert not res_automaton.accepts([b])
    assert not res_automaton.accepts([c])
    assert not res_automaton.accepts([a, b])
    assert not res_automaton.accepts([b, c])


@pytest.fixture(params=[
    (vertices_num, regex)
    for regex in ['a*b*', '(a|b)(c|d)*', 'a* b b* c']
    for vertices_num in [16, 64, 128, 512]
])
def random_data(request):
    vertices_num, regex = request.param
    edges_num = vertices_num * (vertices_num - 1) // 5
    v_from = [random.randint(0, vertices_num) for _ in range(edges_num)]
    v_to = [random.randint(0, vertices_num) for _ in range(edges_num)]
    values = [random.choice(['a', 'b', 'c', 'd']) for _ in range(edges_num)]
    edges = zip(v_from, values, v_to)
    
    dfa = regex_to_dfa(regex)
    query_automaton = Automaton(dfa)

    graph = Graph(edges)
    automaton_graph = Automaton.from_graph(graph) 

    return automaton_graph, query_automaton


def test_intersection_random(random_data):
    graph, regex = random_data
    intersection = graph.get_intersection(regex)

    matrices_res = intersection.adj_matrices

    for label, matrix in matrices_res.items():
        for v_from, v_to in zip(matrix.rows, matrix.cols):
            graph_from, graph_to = v_from // regex.graph.vertices_num, v_to // regex.graph.vertices_num
            regex_from, regex_to = v_from // graph.graph.vertices_num, v_to // graph.graph.vertices_num

            assert matrix[v_from, v_to] == 1
            assert graph.adj_matrices[label][graph_from, graph_to] == 1
            assert regex.adj_matrices[label][regex_from, regex_to] == 1
