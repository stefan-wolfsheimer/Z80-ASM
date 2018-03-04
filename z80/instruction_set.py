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
from z80.instruction import Instruction
from z80.assertions import assert_n
from z80.instructions.general_purpose import NOP2
import importlib
import pkgutil


class InstructionSet(object):
    def __init__(self):
        self.instructions = {}
        # find all instructions
        package = importlib.import_module('z80.instructions')
        for loader, name, is_pkg in pkgutil.walk_packages(package.__path__):
            full_name = package.__name__ + '.' + name
            importlib.import_module(full_name)
        for cls in Instruction.__subclasses__():
            if cls.__name__ != 'NOP2':
                try:
                    cls.register(self)
                    print(cls.__name__)
                except NotImplementedError as e:
                    raise NotImplementedError(cls.__name__ + ":" + str(e))

    def fetch(self, cpu):
        code1 = cpu.GET_ref_PC_plus_d(0)
        if code1 in self.instructions:
            if isinstance(self.instructions[code1], dict):
                code2 = cpu.GET_ref_PC_plus_d(1)
                if code2 in self.instructions[code1]:
                    return self.instructions[code1][code2]
                else:
                    return NOP2()
            else:
                return self.instructions[code1]
        else:
            raise NotImplemented('instruction not implemented %02x' % code1)

    def define_instr(self, code, instr):
        assert_n(code)
        if code in self.instructions:
            raise ValueError('code %x already defined' % code)
        self.instructions[code] = instr

    def define_instr2(self, code1, code2, instr):
        assert_n(code1)
        assert_n(code2)
        if code1 not in self.instructions:
            self.instructions[code1] = {}
        if code2 in self.instructions[code1]:
            raise ValueError('code %x %x already defined' %
                             (code1, code2))
        self.instructions[code1][code2] = instr
