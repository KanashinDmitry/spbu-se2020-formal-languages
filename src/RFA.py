from pygraphblas import Matrix, types
from pyformlang.regular_expression import Regex


class RFA():
    def __init__(self, cfg=None):
        self.start_states = set()
        self.final_states = set()
        self.matrices = dict()
        self.production_heads = {}
        self.vertices_num = 0
        self.start_symbol = None
        if cfg is not None:
            self.create_from_cfg(cfg)

    def create_from_cfg(self, cfg):
        self.vertices_num = sum([len(prod.body) + 1 for prod in cfg.productions])

        curr_index = 0
        for prod in cfg.productions:
            if prod.head.value not in self.matrices.keys():
                self.matrices[prod.head.value] = Matrix.sparse(types.BOOL, self.vertices_num, self.vertices_num)

            start_state = curr_index
            final_state = curr_index + len(prod.body)

            self.start_states.add(start_state)
            self.final_states.add(final_state)

            self.production_heads[(start_state, final_state)] = prod.head.value

            for body_part in prod.body:
                v_from, label, v_to = curr_index, body_part.value, curr_index + 1

                if label not in self.matrices.keys():
                    self.matrices[label] = Matrix.sparse(types.BOOL, self.vertices_num, self.vertices_num)

                self.matrices[label][v_from, v_to] = True

                curr_index += 1

            curr_index += 1

    @classmethod
    def create_from_cfg_regex(cls, name):
        rfa = RFA()
        
        curr_index = 0
        enfas = dict()
        num_production = 0
        productions = []

        with open(name, 'r') as file:
            productions_txt = file.readlines()

            for production_txt in productions_txt:
                line = production_txt.strip().split()
                head, body = line[0], ' '.join(line[1:])
                if rfa.start_symbol is None:
                    rfa.start_symbol = head
                
                enfa = Regex(body.replace('eps', 'epsilon')).to_epsilon_nfa().minimize()
                productions.append(enfa)

                enfas[num_production] = (head, productions[num_production])
                num_production += 1
            
        rfa.vertices_num = sum([len(enfa.states) if len(enfa.states) != 0 else 1 for num, (head, enfa) in enfas.items()])

        for _, (head, enfa) in enfas.items():
            transitions = enfa._transition_function
            
            if list(transitions) == []:                
                rfa.start_states.add(curr_index)
                rfa.final_states.add(curr_index)

                rfa.production_heads[(curr_index, curr_index)] = head

                curr_index += 1

                continue

            states = dict()

            for st_from, symb, st_to in transitions:
                if st_from not in states.keys():
                    states[st_from] = curr_index
                    curr_index += 1

                if st_to not in states.keys():
                    states[st_to] = curr_index
                    curr_index += 1
                    
                v_from, label, v_to = states[st_from], symb.value, states[st_to]

                if label not in rfa.matrices.keys():
                    rfa.matrices[label] = Matrix.sparse(types.BOOL, rfa.vertices_num, rfa.vertices_num)

                rfa.matrices[label][v_from, v_to] = True

            for start_state in enfa.start_states:
                rfa.start_states.add(states[start_state])
                
            for final_state in enfa.final_states:
                rfa.final_states.add(states[final_state])
                rfa.production_heads[(states[enfa.start_state], states[final_state])] = head

        return rfa
