from .register import RegisterPlusOffset


class Instruction(object):
    def __init__(self, assembler, opcode, func, args=[],
                 tstates=1):
        def opcode2offset(i, c):
            if isinstance(c, str) and len(c) == 1:
                return RegisterPlusOffset('PC', i, memonic=c)
            elif isinstance(c, str) and len(c) == 2:
                return RegisterPlusOffset('PC', i, memonic=c, len=2)
            else:
                return c

        self.assembler = assembler
        self.opcode = [opcode2offset(i, c)
                       for i, c in enumerate(opcode)]
        try:
            self.size = sum([1 if isinstance(c, int) else c.len()
                             for c in self.opcode])
        except Exception:
            print(self.opcode)
            raise
        self.func = func
        self.tstates = tstates

    def step(self, cpu):
        pass

    def assembler_to_str(self):
        if len(self.assembler) == 1:
            return self.assembler[0]
        else:
            return self.assembler[0] + " " + ",".join(self.assembler[1:])

    def to_dict(self):
        opcode = []
        opcode_len = 0
        for op in self.opcode:
            if isinstance(op, int):
                opcode.append(op)
                opcode_len += 1
            elif isinstance(op, RegisterPlusOffset):
                opcode.append(op.memonic)
                opcode_len += op.len()

        return {
            'assembler': self.assembler,
            'assembler_str': self.assembler_to_str(),
            'opcode': opcode,
            'opcode_len': opcode_len,
            'tstates': self.tstates
        }
