from pyformlang.cfg import CFG, Variable, Terminal, Production
from typing import List, Set


class CFGrammar:
    def __init__(self, name):
        self.cfg = CFGrammar.read_grammar(name)
        self.eps = self.cfg.generate_epsilon()
        self.cnf = self.cfg.to_normal_form()

    def cyk(self, word):
        word_size = len(word)

        if word_size == 0:
            return self.eps

        cfg = self.cnf
        productions = cfg.productions

        cyk_table = [[set() for _ in range(word_size)] for _ in range(word_size)]

        for index, letter in enumerate(word):
            for production in productions:
                if len(production.body) == 1 \
                   and production.body[0] == Terminal(letter):
                    cyk_table[index][index].add(production.head)

        for level in range(1, word_size):
            for production_index in range(word_size - level):
                row = production_index
                column = level + production_index

                for col_new in range(row, column):
                    row_new = col_new + 1

                    body_left = cyk_table[row][col_new]
                    body_right = cyk_table[row_new][column]

                    for production in productions:
                        if len(production.body) == 2 \
                           and production.body[0] in body_left \
                           and production.body[1] in body_right:
                            cyk_table[row][column].add(production.head)

        start_symbol_table = cyk_table[0][word_size - 1]

        if len(start_symbol_table) != 0:
            return cfg.start_symbol in start_symbol_table

        return False

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

                productions.add(Production(Variable(head), body_cfg))

        cfg = CFG(non_terminals, terminals, start_symb, productions)

        return cfg
