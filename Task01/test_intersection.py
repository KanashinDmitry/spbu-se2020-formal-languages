import pytest
from pyformlang.finite_automaton import EpsilonNFA, State, Symbol, Epsilon


def test_check_intersection():
    # Declare NFAs
    enfa0 = EpsilonNFA()
    enfa1 = EpsilonNFA()

    # Declare the states
    states = [State("q" + str(x)) for x in range(7)]

    # Declare the symbols
    epsilon = Epsilon()
    symb_a = Symbol("a")
    symb_b = Symbol("b")
    symb_c = Symbol("c")

    # epsilonNFA 0
    # Add a start state
    enfa0.add_start_state(states[0])

    # Add a final state
    enfa0.add_final_state(states[1])

    # Add the transitions
    enfa0.add_transition(states[0], symb_a, states[1])
    enfa0.add_transition(states[1], symb_a, states[1])

    # epsilonNFA 1
    # Add a start states
    enfa1.add_start_state(states[0])
    enfa1.add_final_state(states[4])

    # Add a final states
    enfa1.add_final_state(states[5])
    enfa1.add_final_state(states[6])

    # Add the transitions
    enfa1.add_transition(states[0], symb_a, states[1])
    enfa1.add_transition(states[0], symb_b, states[2])
    enfa1.add_transition(states[0], symb_c, states[3])

    enfa1.add_transition(states[1], symb_a, states[4])
    enfa1.add_transition(states[2], symb_b, states[5])
    enfa1.add_transition(states[3], symb_c, states[6])

    # Now enfa0 accepts a* \ {epsilon}
    #     enfa1 accepts aa, bb, cc

    # Intersection of enfa0 and enfa1
    enfa_res = enfa0.get_intersection(enfa1)

    # Check if a word is accepted
    assert enfa_res.accepts([symb_a, symb_a]), "Should accept aa"

    # Check non-correct words
    assert not enfa_res.accepts([epsilon]), "Accepts empty word, but it mustn't"
    assert not enfa_res.accepts([symb_a, symb_a, symb_a]), "Accepts aaa, but it mustn't"
    assert not enfa_res.accepts([symb_a]), "Accepts a, but it mustn't"
    assert not enfa_res.accepts([symb_b, symb_b]), "Accepts bb, but it mustn't"
    assert not enfa_res.accepts([symb_c, symb_c]), "Accepts cc, but it mustn't"
