import re
from functools import wraps
from instruction import Instruction

REGISTER_CODE = {'r': {'A': '111',
                       'B': '000',
                       'C': '001',
                       'D': '010',
                       'E': '011',
                       'H': '100',
                       'L': '101'},
                 'b': {'0': '000',
                       '1': '001',
                       '2': '010',
                       '3': '011',
                       '4': '100',
                       '5': '101',
                       '6': '110',
                       '7': '111'},
                 "dd": {'BC': '00',
                        'DE': '01',
                        'HL': '10',
                        'SP': '11'},
                 "qq": {'BC': '00',
                        'DE': '01',
                        'HL': '10',
                        'AF': '11'},
                 "ss": {'BC': '00',
                        'DE': '01',
                        'HL': '10',
                        'SP': '11'},
                 "pp": {'BC': '00',
                        'DE': '01',
                        'IX': '10',
                        'SP': '11'},
                 "rr": {'BC': '00',
                        'DE': '01',
                        'IY': '10',
                        'SP': '11'},
                 "ii": {'IX': '011',
                        'IY': '111'}}


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


def encode_opcode(pattern, codes):
    ret = []
    for p in pattern:
        if isinstance(p, int):
            ret.append(p)
        elif re.match('^[0-9{}]+$', p):
            ret.append(int(p.format(*codes), 2))
        else:
            ret.append(p)
    return ret


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
                                 for arg in res.groups()[2::2]
                                 if arg is not None]
    else:
        raise ValueError('invalid function name {0}'.format(func_name))


class InstructionTemplate(object):
    def __init__(self, group, opcode, expand=None,
                 tstates=None, assembler=None):
        self.group = group
        self.opcode = opcode if isinstance(opcode, list) else [opcode]
        self.expand = [] if expand is None else expand
        self.tstates = 1 if tstates is None else tstates
        self.assembler = assembler
        self.instructions = []

    def __call__(self, func):
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
                assembler = self.assembler
            self.instructions.append(Instruction(assembler,
                                                 encode_opcode(self.opcode,
                                                               codes),
                                                 func,
                                                 args=list(regs),
                                                 tstates=self.tstates))

        if self.assembler is None:
            self.assembler = function_name_to_assembler(name,
                                                        zip(self.expand,
                                                            self.expand))
        self.group.add(self)
        return wrapper