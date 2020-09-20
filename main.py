import sys
from src.Automaton import Automaton
from src.Graph import Graph
from src.Utils import *  
import argparse     


def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument(
        "graph_path",
        help=('File with edge list. '
              'Format: <vertice> <label> <vertice>')
    )
    parser.add_argument(
        "regex_path",
        help=('File with regexp')
    )
    parser.add_argument(
        "--from_v_path",
        dest="start_vertices_path",
        help=('Path of file with set of starting vertices.'),
        required=False
    )
    parser.add_argument(
        "--to_v_path",
        dest="end_vertices_path",
        help=('Path of file with set of ending (final) vertices set.'),
        required=False
    )

    args = parser.parse_args()

    edges = read_graph(args.graph_path)
    regex = read_regex(args.regex_path)
    
    start_v = []
    if args.start_vertices_path is not None:
        start_v = list(map(int, read_vertices(args.start_vertices_path)))

    end_v = []
    if args.end_vertices_path is not None:
        end_v = list(map(int, read_vertices(args.end_vertices_path)))

    dfa = regex_to_dfa(regex)
    query_automaton = Automaton(dfa)

    graph = Graph(edges)
    automaton_graph = Automaton.from_graph(graph)

    if start_v != []:
        if end_v != []:
            automaton_graph.reach_from_to(query_automaton, start_v, end_v)
        else:
            automaton_graph.reach_from(query_automaton, start_v)
    else:
        automaton_graph.reach_all(query_automaton)

    res = automaton_graph.get_intersection(query_automaton)
    matrices_res = res.adj_matrices
    for label, matrix in matrices_res.items():
        print(f'{label} {matrix.nvals}')

    return 0


if __name__ == '__main__':
    main()
