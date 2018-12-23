from register import RegisterPlusOffset


class Instruction(object):
    def __init__(self, assembler, opcode, func, args=[],
                 tstates=1, operation="", group=""):
        def opcode2offset(i, c):
            if isinstance(c, str) and len(c) == 1:
                return RegisterPlusOffset('PC', i, memonic=c)
            elif isinstance(c, str) and len(c) == 2:
                return RegisterPlusOffset('PC', i, memonic=c, len=2)
            else:
                return c

        self.instr = assembler
        self.opcode = [opcode2offset(i, c)
                       for i, c in enumerate(opcode)]
        try:
            self.size = sum([1 if isinstance(c, int) else c.len()
                             for c in self.opcode])
        except Exception:
            import pprint
            pprint.pprint(self.opcode)
            raise
        self.func = func
        self.tstates = tstates
        self.operation = operation
        self.fmt = assembler[0]
        if len(assembler[1:]) > 0:
            self.fmt += " " + ",".join(assembler[1:])
        self.group = group

    def step(self, cpu):
        pass

    def format(self):
        return self.fmt
