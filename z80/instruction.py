class Instruction(object):
    def __init__(self, assembler, opcode, func,
                 tstates=1, operation="", group=""):
        self.instr = assembler
        self.opcode = opcode
        self.size = len(opcode)
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
