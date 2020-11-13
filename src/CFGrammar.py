from pyformlang.cfg import CFG, Variable, Terminal, Production
from typing import List, Set
from src.Utils import read_tokens
import os


class CFGrammar:
    def __init__(self, name=None, cfg=None):
        if name is not None:
            self.cfg = CFGrammar.read_grammar(name)
        elif cfg is not None:
            self.cfg = cfg
        self.eps = self.cfg.generate_epsilon()
        self.cnf = self.cfg.to_normal_form()

    def cyk(self, words, tokens=dict()):
        word_size = sum([1 if word in tokens.keys() else len(word) for word in words.split()])

        if word_size == 0:
            return self.eps

        cfg = self.cnf
        productions = cfg.productions

        cyk_table = [[set() for _ in range(word_size)] for _ in range(word_size)]

        shift = 0
        for word in words.split():
            if word in tokens.keys():
                for production in productions:
                    if len(production.body) == 1 \
                    and production.body[0] == Terminal(tokens[word]):
                        cyk_table[shift][shift].add(production.head)
                shift += 1
            else:
                for index, letter in enumerate(word):
                    for production in productions:
                        if len(production.body) == 1 \
                        and production.body[0] == Terminal(letter):
                            cyk_table[shift + index][shift + index].add(production.head)
                shift += len(word)
            
        productions_len_2 = [prod for prod in productions if len(prod.body) == 2]

        for level in range(1, word_size):
            for production_index in range(word_size - level):
                row = production_index
                column = level + production_index

                for col_new in range(row, column):
                    row_new = col_new + 1

                    body_left = cyk_table[row][col_new]
                    body_right = cyk_table[row_new][column]

                    for production in productions_len_2:
                        if production.body[0] in body_left \
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


    @classmethod
    def read_grammar_with_tokens(cls, name_g, name_t):
        tokens = read_tokens(name_t)

        terminals, non_terminals, productions = set(), set(), set()

        with open(name_g, 'r') as file:
            productions_txt = file.readlines()

            for production_txt in productions_txt:
                head, _, *body = production_txt.strip().split()
                print(head, body)
                

    @classmethod
    def read_production_regex(cls, head, regex, id, case_sens=True):
        var_by_state = dict()
        terminals, variables, productions = set(), set(), set()
        
        enfa = regex.to_epsilon_nfa().minimize()

        if len(enfa.states) == 0:
            variables.add(head)
            productions.add(Production(head, [Epsilon()]))
            return productions, variables, terminals, id

        for state in enfa.states:
            var_by_state[state] = Variable(f'Id{id},{state}')
            id += 1

        transitions = enfa._transition_function
              
        for start_st in enfa.start_states:
            productions.add(Production(head, [var_by_state[start_st]]))


        for st_from, symb, st_to in transitions:
            new_head = var_by_state[st_from]
            new_body = []

            value = symb.value

            if value == 'eps':
                new_body.append(Epsilon())
            elif value.isupper() and case_sens:
                variable = Variable(value)
                new_body.append(variable)
                variables.add(variable)
            elif value.isdigit() or value.islower() or not case_sens:
                variable = Terminal(value)
                new_body.append(variable)
                variables.add(variable)
            else:
                raise ValueError(f'Symbol "{value}" should be either lower or upper case')
            
            new_body.append(var_by_state[st_to])

            productions.add(Production(new_head, new_body))
            
            if st_to in enfa.final_states:
                productions.add(Production(var_by_state[st_to], []))
        
        return productions, variables, terminals, id
