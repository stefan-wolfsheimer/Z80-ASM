from .register import PC


class InstructionSet(object):
    def __init__(self):
        self.instructions = {}
        self.groups = []

    def __getitem__(self, key):
        return self.instructions[key]

    def __contains__(self, key):
        return key in self.instructions

    def add_group(self, group):
        self.groups.append(group)

    def add(self, instr):
        def set_code(instructions, codes, instr):
            if len(codes) == 1:
                instructions[codes[0]] = instr
            else:
                if not codes[0] in instructions:
                    instructions[codes[0]] = {}
                set_code(instructions[codes[0]], codes[1:], instr)

        set_code(self.instructions, instr.opcode, instr)

    def fetch(self, cpu):
        code1 = cpu[PC()]
        if code1 in self:
            if isinstance(self[code1], dict):
                code2 = self[PC(1)]
                if code2 in self[code1]:
                    instr = self[code1][code2]
                    import pprint
                    pprint.pprint(vars(instr))
                    return instr
                else:
                    return None
            else:
                instr = self[code1]
                import pprint
                pprint.pprint(vars(instr))
                return self[code1]
        else:
            raise NotImplemented('instruction not implemented %02x' % code1)
