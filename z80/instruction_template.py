import re
from functools import wraps
from .instruction import Instruction


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
FUNCTION_NAME_TO_ASSEMBLER_PATTERN = re.compile('^([a-zA-Z]+){0}{0}$'.
                                                format(FUNCTION_ARGUMENT))
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


def function_name_to_assembler(func_name):
    def transform_indirect_addr(arg):
        for expr, repl in FUNCTION_NAME_INDIRECT_ADDR_PATTERN:
            if expr.match(arg):
                return expr.sub(repl, arg)
        return arg

    res = FUNCTION_NAME_TO_ASSEMBLER_PATTERN.match(func_name)
    if res is not None:
        assembler = [res.group(1)] +\
                    [transform_indirect_addr(a)
                     for a in res.groups()[2::2]
                     if a is not None]
        return assembler
    else:
        raise ValueError('invalid function name {0}'.format(func_name))


def expand_assembler(assembler, expand):
    ret = [assembler[0]]
    for arg in assembler[1:]:
        if len(expand) and expand[0][0] in arg:
            ret.append(arg.replace(*expand.pop(0)))
        else:
            ret.append(arg)
    return ret


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

        if self.assembler is None:
            self.assembler = function_name_to_assembler(func.__name__)

        for regs, codes in enum_register_codes(self.expand):
            assembler = expand_assembler(self.assembler,
                                         list(zip(self.expand, regs)))
            self.instructions.append(Instruction(assembler,
                                                 encode_opcode(self.opcode,
                                                               codes),
                                                 func,
                                                 args=list(regs),
                                                 tstates=self.tstates))
        self.group.add(self)
        return wrapper

    def assembler_to_str(self):
        if len(self.assembler) == 1:
            return self.assembler[0]
        else:
            return self.assembler[0] + " " + ",".join(self.assembler[1:])

    def to_dict(self):
        return {
            'opcode': self.opcode,
            'expand': self.expand,
            'tstates': self.tstates,
            'assembler': self.assembler,
            'assembler_str': self.assembler_to_str(),
            'instructions': [i.to_dict() for i in self.instructions]}
