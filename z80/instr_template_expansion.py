# MIT License

# Copyright (c) 2018 stefan-wolfsheimer

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# from z80.instructions import Instruction
import re


REGISTER_CODE = {'r': {'A': '111',
                       'B': '000',
                       'C': '001',
                       'D': '010',
                       'E': '011',
                       'H': '100',
                       'L': '101'},
                 "dd": {'BC': '00',
                        'DE': '01',
                        'HL': '10',
                        'SP': '11'},
                 "qq": {'BC': '00',
                        'DE': '01',
                        'HL': '10',
                        'AF': '11'},
                 "ii": {'IX': '011',
                        'IY': '111'}}


def scan_asm(instr_str):
    """
    tokenize the instruction into
    INSTR or INSTR ARG or INSTR ARG, ARG
    returns a tuple of size 1,2 or 3 respectively
    """
    arg_patt = '\\S+|\\(.*\\)'
    patt = re.compile('^\\s*([a-zA-Z]+)' +
                      '(\\s+(' + arg_patt + ')\\s*' +
                      '(,\\s*(' + arg_patt + '))?)?\\s*$')
    res = patt.match(instr_str)
    if res is not None:
        if res.group(3) is None:
            return (res.group(1).strip(),)
        elif res.group(5) is None:
            return (res.group(1).strip(),
                    res.group(3).strip())
        else:
            return (res.group(1).strip(),
                    res.group(3).strip(),
                    res.group(5).strip())
    else:
        return None


def extract_register_codes(instr):
    def get_reg_name(arg, register_codes):
        reg = arg.replace(' ', '')
        if reg == '(ii+d)':
            reg = 'ii'
        if reg in REGISTER_CODE:
            i = len(register_codes)
            register_codes = register_codes + (reg,)
            return (register_codes, arg.replace(reg, "{%d}" % i))
        else:
            return (register_codes, arg)

    if len(instr) == 1:
        return ((), instr[0])
    elif len(instr) >= 2:
        register_codes = ()
        (register_codes, arg1) = get_reg_name(instr[1], register_codes)
        if len(instr) == 3:
            (register_codes, arg2) = get_reg_name(instr[2], register_codes)
            return (register_codes, instr[0], arg1, arg2)
        else:
            return (register_codes, instr[0], arg1)


def enum_register_codes(r_codes):
    if len(r_codes) == 0:
        return [((), ())]
    else:
        return [((name,) + name_rhs, (code,) + code_rhs)
                for (name, code) in REGISTER_CODE[r_codes[0]].items()
                for (name_rhs, code_rhs) in enum_register_codes(r_codes[1:])]


def expand_template(entry):
    def encode_opt(opt, codes):
        if isinstance(opt, int):
            return opt
        elif re.match('^[0-9{}]+$', opt):
            return int(opt.format(*codes), 2)
        else:
            return opt

    def apply_template(entry, names, codes):
        opt_tuple = entry[1] if isinstance(entry[1], tuple) else (entry[1],)
        return {'instr': tuple([x.format(*names) for x in entry[0]]),
                'opcode': tuple([encode_opt(x, codes) for x in opt_tuple]),
                'tstates': entry[2],
                'operation': entry[3].format(*names),
                'func': lambda cpu: entry[4](cpu, *names)}

    instr = extract_register_codes(scan_asm(entry[0]))
    codes = enum_register_codes(instr[0])
    return [apply_template((instr[1:],) + entry[1:], names, codes)
            for names, codes in codes]
