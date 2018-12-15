import re
from functools import wraps
from instr_template_expansion import REGISTER_CODE
from instruction import Instruction


FUNCTION_ARGUMENT = '(_([a-zA-Z]{1,2}|_[a-zA-Z]{2}_|_ii_d_))?'
FUNCTION_NAME_TO_ASSEMBLER_PATTERN = re.compile('^([a-zA-Z]+)' +
                                                FUNCTION_ARGUMENT +
                                                FUNCTION_ARGUMENT + '$')
FUNCTION_NAME_INDIRECT_ADDR_PATTERN = [(re.compile('^_([a-zA-Z]{2})_$'),
                                        r'(\1)'),
                                       (re.compile('^_([a-zA-Z]{2})_(d)_$'),
                                        r'(\1+d)')]


def enum_register_codes(r_codes):
    if len(r_codes) == 0:
        return [((), ())]
    else:
        return [((name,) + name_rhs, (code,) + code_rhs)
                for (name, code) in REGISTER_CODE[r_codes[0]].items()
                for (name_rhs, code_rhs) in enum_register_codes(r_codes[1:])]


def function_name_to_assembler(func_name, expand):
    def transform_indirect_addr(arg):
        for expr, repl in FUNCTION_NAME_INDIRECT_ADDR_PATTERN:
            if expr.match(arg):
                return expr.sub(repl, arg)
        return arg

    def transform_arg(arg):
        if len(expand) and expand[0][0] in arg:
            return transform_indirect_addr(arg.replace(*expand.pop(0)))
        else:
            return transform_indirect_addr(arg)

    res = FUNCTION_NAME_TO_ASSEMBLER_PATTERN.match(func_name)
    if res is not None:
        return [res.group(1)] + [transform_arg(arg)
                                 for arg in res.groups()[2::2]]
    else:
        raise ValueError('invalid function name {0}'.format(func_name))


class InstructionDecor(object):
    def __init__(self, group, opcode, expand=None,
                 tstates=None, assembler=None):
        self.group = group
        self.opcode = opcode if isinstance(opcode, list) else [opcode]
        self.expand = [] if expand is None else expand
        self.tstates = 1 if tstates is None else tstates
        self.assembler = assembler

    def __call__(self, func):
        def encode_opcode(opt, codes):
            if isinstance(opt, int):
                return opt
            elif re.match('^[0-9{}]+$', opt):
                return int(opt.format(*codes), 2)
            else:
                return opt

        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        name = func.__name__

        for regs, codes in enum_register_codes(self.expand):
            if self.assembler is None:
                assembler = function_name_to_assembler(name,
                                                       zip(self.expand,
                                                           regs))
            else:
                assembler = self.instr
            args = list(regs)
            instr = Instruction(assembler,
                                [encode_opcode(c, codes) for c in self.opcode],
                                func,
                                args=args,
                                tstates=self.tstates,
                                operation="",
                                group=self.group.name)
            self.group.add(instr)

        return wrapper


class InstructionGroup(object):
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.instructions = {}

    def __getitem__(self, key):
        return self.instructions[key]

    def __contains__(self, key):
        return key in self.instructions

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