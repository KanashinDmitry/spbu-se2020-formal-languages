from pyformlang.cfg import CFG, Variable, Terminal, Production, Epsilon
from typing import List, Set

class CFGrammar:
    eps: bool
    
    def __init__(self, name):
        self.cfg = CFGrammar.read_grammar(name)
        self.eps = self.cfg.generate_epsilon()
        self.cnf = self.cfg.to_normal_form()
        self.wcnf = self.to_weak_cnf()

    #cyk
    def cyk(self, word):
        cfg = self.cnf
        productions = cfg.productions

        word_size = len(word)
        cyk_table: List[List[Set]] = [[set() for _ in range(word_size)] for _ in range(word_size) ]
        
        if word_size == 0:
            return self.eps

        for index, letter in enumerate(word):
            for production in productions:
                if production.body == [Terminal(letter)]:
                    cyk_table[index][index].add(production.head)

      
        for level in range(1, word_size):      
            for production_index in range(word_size - level):
                row = production_index
                column = level + production_index
                
                for col_new in range(row, column):
                    row_new = col_new + 1

                    body = cyk_table[row][col_new] | cyk_table[row_new][column]

                    for production in productions:
                        if set(production.body) == body:
                            cyk_table[row][column].add(production.head)

        start_symbol_table = cyk_table[0][word_size - 1]

        if len(start_symbol_table) != 0: 
            return start_symbol_table == {cfg.start_symbol}
        
        return False

    def to_weak_cnf(self):
        cfg = self.cfg
        return cfg.to_normal_form()

    def is_word_in_cfg_hemming(self, graph):
        cfg = self.cfg
        return 0                     
                        
    @classmethod
    def read_grammar(cls, name):
        terminals, non_terminals, productions = set(), set(), set()
        start_symb = None

        with open(name, 'r') as file:
            productions_txt = file.readlines()

            for production_txt in productions_txt:
                head, *body = production_txt.strip().split()
                
                if start_symb is None:
                    start_symb = Variable(head)
                
                body_cfg = []
                for letter in body:
                        if letter.isupper():
                            non_terminal = Variable(letter)
                            non_terminals.add(non_terminal)
                            body_cfg.append(non_terminal)
                        else:
                            terminal = Terminal(letter)
                            terminals.add(terminal)
                            body_cfg.append(terminal)

                #print("Epsilon" if body == [] else body)
                #print(body == [])
                #print(Production(Variable(head), [Epsilon()] if body == [] else body_cfg))

                productions.add(Production(Variable(head), [Epsilon()] if body == [] else body_cfg))

        cfg = CFG(non_terminals, terminals, start_symb, productions)

        return cfg
