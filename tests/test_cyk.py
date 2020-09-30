import os
from src.CFGrammar import CFGrammar

DATA_PATH = os.path.join(os.getcwd(), 'tests/data/cyk')


def test_parentheses():
    cfg_wrapper = CFGrammar(os.path.join(DATA_PATH, "grammar_1_parentheses.txt"))

    should_accept = ["ab", "aabb", ""]
    should_not_accept = ["aab", "abb", "a ", "b"]
    
    for word in should_accept:
        assert cfg_wrapper.cyk(word)

    for word in should_not_accept:
        assert not cfg_wrapper.cyk(word)

# palindrome wcw^(-1)
def test_palindrome():
    cfg_wrapper = CFGrammar(os.path.join(DATA_PATH, "grammar_2_palindrome.txt"))

    should_accept = ["tenet", "tnt", "ene", "n", "teeneet", "ttenett"]
    should_not_accept = ["tt", "ee", "teet", "enet", "tene", "tnet", "tent", ""]

    for word in should_accept:
        assert cfg_wrapper.cyk(word)

    for word in should_not_accept:
        assert not cfg_wrapper.cyk(word)
