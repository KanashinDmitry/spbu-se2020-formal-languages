import os
from src.CFGrammar import CFGrammar

DATA_PATH = os.path.join(os.getcwd(), 'tests/data/cyk')


def test_parentheses():
    cfg_wrapper = CFGrammar(os.path.join(DATA_PATH, "grammar_1_parentheses.txt"))
    
    assert cfg_wrapper.cyk("ab")
    assert cfg_wrapper.cyk("aabb")
    assert cfg_wrapper.cyk("")

    assert not cfg_wrapper.cyk("aab")
    assert not cfg_wrapper.cyk("abb")
    assert not cfg_wrapper.cyk("a")
    assert not cfg_wrapper.cyk("b")

# palindrome wcw^(-1)
def test_palindrome():
    cfg_wrapper = CFGrammar(os.path.join(DATA_PATH, "grammar_2_palindrome.txt"))

    assert cfg_wrapper.cyk("tenet")
    assert cfg_wrapper.cyk("tnt")
    assert cfg_wrapper.cyk("ene")
    assert cfg_wrapper.cyk("n")
    assert cfg_wrapper.cyk("teeneet")
    assert cfg_wrapper.cyk("ttenett")

    assert not cfg_wrapper.cyk("tt")
    assert not cfg_wrapper.cyk("ee")
    assert not cfg_wrapper.cyk("teet")
    assert not cfg_wrapper.cyk("enet")
    assert not cfg_wrapper.cyk("tene")
    assert not cfg_wrapper.cyk("tnet")
    assert not cfg_wrapper.cyk("tent")
    assert not cfg_wrapper.cyk("")

# same grammar like for hellings a*b(a|b)*
def test_3():
    cfg_wrapper = CFGrammar(os.path.join(DATA_PATH, "grammar_3.txt"))

    assert cfg_wrapper.cyk("b")
    assert cfg_wrapper.cyk("ab")
    assert cfg_wrapper.cyk("ba")
    assert cfg_wrapper.cyk("bb")
    assert cfg_wrapper.cyk("aba")
    assert cfg_wrapper.cyk("abb")
    assert cfg_wrapper.cyk("aab")
    assert cfg_wrapper.cyk("baa")
    assert cfg_wrapper.cyk("bbb")
    assert cfg_wrapper.cyk("bab")
    assert cfg_wrapper.cyk("bba")
    assert cfg_wrapper.cyk("abab")
    assert cfg_wrapper.cyk("abba")

    assert not cfg_wrapper.cyk("a")
    assert not cfg_wrapper.cyk("aa")
    assert not cfg_wrapper.cyk("")
