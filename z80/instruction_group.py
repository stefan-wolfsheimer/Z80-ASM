from functools import wraps
from instr_template_expansion import REGISTER_CODE
from instruction import Instruction


def enum_register_codes(r_codes):
    if len(r_codes) == 0:
        return [((), ())]
    else:
        return [((name,) + name_rhs, (code,) + code_rhs)
                for (name, code) in REGISTER_CODE[r_codes[0]].items()
                for (name_rhs, code_rhs) in enum_register_codes(r_codes[1:])]


def function_name_to_assembler(func_name, expand):
    a = func_name.split("_")
    return [a[0]] + [arg.replace(*repl) if len(repl) else arg
                     for arg, repl in zip(a[1:], expand)]


class InstructionDecor(object):
    def __init__(self, group, opcode, expand=None,
                 tstates=None, assembler=None):
        self.group = group
        self.opcode = opcode if isinstance(opcode, list) else [opcode]
        self.expand = [] if expand is None else expand
        self.tstates = 1 if tstates is None else tstates
        self.assembler = assembler

    def __call__(self, func):
        name = func.__name__

        for regs, codes in enum_register_codes(self.expand):
            opcode = [c if isinstance(c, int) else int(c.format(*codes), 2)
                      for c in self.opcode]
            if self.assembler is None:
                assembler = function_name_to_assembler(name,
                                                       zip(self.expand,
                                                           regs))
            else:
                assembler = self.instr
            instr = Instruction(assembler, opcode, func,
                                tstates=self.tstates,
                                operation="",
                                group=self.group.name)
            self.group.add(instr)

        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper


class InstructionGroup(object):
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.instructions = {}

    def add(self, instr):
        def set_code(instructions, codes, instr):
            if len(codes) == 1:
                instructions[codes[0]] = instr
            else:
                if not codes[0] in instructions:
                    instructions[codes[0]] = {}
                set_code(instructions[codes[0]], codes[1:], instr)

        if self.parent is not None:
            self.parent.add(instr)

        set_code(self.instructions, instr.opcode, instr)
