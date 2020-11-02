from pyformlang.cfg import CFG, Terminal, Variable
from pygraphblas import types, Matrix, semiring
from src.CFGrammar import CFGrammar
from src.RFA import RFA
from src.AdjMatrix import AdjMatrix
from src.Graph import Graph


def cfpq_hellings(graph: Graph, cfg: CFGrammar):
    query = cfg.cfg
    edges = graph.edges
    reachable_pairs = set()

    if cfg.eps:
        for v in graph.vertices:
            reachable_pairs.add((query.start_symbol, v, v))

    query = cfg.cnf

    for v, terminal, u in edges:
        for production in query.productions:
            if len(production.body) == 1 \
               and production.body[0] == Terminal(terminal):
                reachable_pairs.add((production.head, v, u))

    working_set = reachable_pairs.copy()

    productions_len_2 = set([production for production in query.productions
                                        if len(production.body) == 2])

    while len(working_set) != 0:
        variable, v_from, v_to = working_set.pop()

        new_pairs = set()

        for variable_left, left_v_from, v_new in reachable_pairs:
            if v_new == v_from:
                for production in productions_len_2:
                    if not (production.head, left_v_from, v_to) in reachable_pairs \
                       and variable_left == production.body[0] \
                       and variable == production.body[1]:
                        new_pairs.add((production.head, left_v_from, v_to))

        for variable_right, v_new, right_v_to in reachable_pairs:
            if v_new == v_to:
                for production in productions_len_2:
                    if not (production.head, v_from, right_v_to) in reachable_pairs \
                       and variable == production.body[0] \
                       and variable_right == production.body[1]:
                        new_pairs.add((production.head, v_from, right_v_to))

        working_set |= new_pairs
        reachable_pairs |= new_pairs

    result = [(v_from, v_to) for variable, v_from, v_to in reachable_pairs
                             if variable == query.start_symbol]

    return result


def cfpq_matrices(graph: Graph, cfg_wrapper: CFGrammar):
    query = cfg_wrapper.cfg
    v_num = graph.vertices_num
    edges = graph.edges
    res_matrices = dict()

    # matrix initialization
    if cfg_wrapper.eps:
        for production in query.productions:
            if production.head not in res_matrices.keys():
                res_matrices[production.head] = Matrix.sparse(types.BOOL, v_num, v_num)
            if production.body == []:
                for vertice in graph.vertices:
                    res_matrices[production.head][vertice, vertice] = 1

    query = cfg_wrapper.cnf

    for v_from, label, v_to in edges:
        for production in query.productions:
            if len(production.body) == 1 and production.body[0] == Terminal(label):
                if production.head not in res_matrices.keys():
                    res_matrices[production.head] = Matrix.sparse(types.BOOL, v_num, v_num)
                res_matrices[production.head][v_from, v_to] = 1

    # nonterm productions
    productions_len_2 = set([production for production in query.productions if len(production.body) == 2])

    # main cycle
    changing = True
    with semiring.LOR_LAND_BOOL:
        while changing:
            changing = False

            for production in productions_len_2:
                body = production.body
                head = production.head

                if body[0] not in res_matrices.keys() or body[1] not in res_matrices.keys():
                    continue
                if head not in res_matrices.keys():
                    res_matrices[head] = Matrix.sparse(types.BOOL, v_num, v_num)

                head_prev_m_nvals = res_matrices[head].nvals

                res_matrices[head] += res_matrices[body[0]] @ res_matrices[body[1]]

                changing |= head_prev_m_nvals != res_matrices[head].nvals

    result = [(v_from, v_to) for v_from, v_to, _ in zip(*res_matrices[query.start_symbol].to_lists())]

    return result


def cfpq_tensor_base(graph: Graph, cfg_wrapper: CFGrammar, is_cnf):
    if graph.vertices_num == 0:
        return []

    res = AdjMatrix(graph).M_bin

    query = cfg_wrapper.cnf if is_cnf else cfg_wrapper.cfg

    rfa = RFA(query)
                    
    if cfg_wrapper.eps:
        res[query.start_symbol] = Matrix.sparse(types.BOOL, graph.vertices_num, graph.vertices_num)
            
        for vertice in graph.vertices:
            res[query.start_symbol][vertice, vertice] = True

    for production in query.productions:
        label = production.head.value
        if label not in res.keys():
            res[label] = Matrix.sparse(types.BOOL, graph.vertices_num, graph.vertices_num)

        if not (is_cnf or production.body) :
            for vertice in graph.vertices:
                res[label][vertice, vertice] = True

    changing = True
    while changing:
        changing = False

        num_v_intersection = rfa.vertices_num * graph.vertices_num

        intersection = AdjMatrix.adj_kronecker(rfa.matrices, res)

        full_m_intersection = AdjMatrix.merge_label_matrices(intersection, num_v_intersection)
        closure = AdjMatrix.transitive_closure(full_m_intersection)

        for v_from, v_to in AdjMatrix.reachable_vertices(closure):
            rfa_from, rfa_to = v_from // graph.vertices_num, v_to // graph.vertices_num
            graph_from, graph_to = v_from % graph.vertices_num, v_to % graph.vertices_num

            if rfa_from in rfa.start_states and rfa_to in rfa.final_states:
                label = rfa.production_heads[(rfa_from, rfa_to)]
                if not res[label].get(graph_from, graph_to, False):
                    changing = True
                res[label][graph_from, graph_to] = True

    result = [(v_from, v_to) for v_from, v_to, _ in zip(*res[query.start_symbol.value].to_lists())]

    return result


def cfpq_tensor_with_rfa(graph: Graph, rfa: RFA):
    if graph.vertices_num == 0:
        return []

    res = AdjMatrix(graph).M_bin    

    for (st_from, st_to), head in rfa.production_heads.items():

        if head not in res.keys():
            res[head] = Matrix.sparse(types.BOOL, graph.vertices_num, graph.vertices_num)

        if st_from == st_to:
           for vertice in graph.vertices:
                   res[head][vertice, vertice] = True

    changing = True
    while changing:
        changing = False

        num_v_intersection = rfa.vertices_num * graph.vertices_num

        intersection = AdjMatrix.adj_kronecker(rfa.matrices, res)

        full_m_intersection = AdjMatrix.merge_label_matrices(intersection, num_v_intersection)
        closure = AdjMatrix.transitive_closure(full_m_intersection)

        for v_from, v_to in AdjMatrix.reachable_vertices(closure):
            rfa_from, rfa_to = v_from // graph.vertices_num, v_to // graph.vertices_num
            graph_from, graph_to = v_from % graph.vertices_num, v_to % graph.vertices_num

            if rfa_from in rfa.start_states and rfa_to in rfa.final_states:
                label = rfa.production_heads[(rfa_from, rfa_to)]
                if not res[label].get(graph_from, graph_to, False):
                    changing = True
                res[label][graph_from, graph_to] = True

    result = [(v_from, v_to) for v_from, v_to, _ in zip(*res[rfa.start_symbol].to_lists())]

    return result


def cfpq_tensor(graph: Graph, cfg_wrapper: CFGrammar):
    return cfpq_tensor_base(graph, cfg_wrapper, is_cnf=False)


def cfpq_tensor_wcnf(graph: Graph, cfg_wrapper: CFGrammar):
    return cfpq_tensor_base(graph, cfg_wrapper, is_cnf=True)
