from pygraphblas import Matrix, types


class RFA():
    def __init__(self, cfg):
        self.start_states = set()
        self.final_states = set()
        self.matrices = dict()
        self.production_heads = {}
        self.vertices_num = 0
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
