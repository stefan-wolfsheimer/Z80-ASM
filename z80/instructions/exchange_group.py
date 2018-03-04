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
from z80.instruction import Instruction
from z80.assertions import assert_index


class EX_DE_HL(Instruction):
    def __init__(self):
        self.fmt = "EX DE, HL"
        self.size = 1

    @staticmethod
    def register(iset):
        iset.define_instr(0xeb, EX_DE_HL())

    def step(self, cpu):
        tmp = cpu.GET_DE()
        cpu.LD_ii_nn('DE', cpu.GET_HL())
        cpu.LD_ii_nn('HL', tmp)


class EX_AF_altAF(Instruction):
    def __init__(self):
        self.fmt = "EX AF, AF'"
        self.size = 1

    @staticmethod
    def register(iset):
        iset.define_instr(0x08, EX_AF_altAF())

    def step(self, cpu):
        cpu.EX_q_altq('A')
        cpu.EX_q_altq('F')


class EXX(Instruction):
    def __init__(self):
        self.fmt = "EXX"
        self.size = 1

    @staticmethod
    def register(iset):
        iset.define_instr(0xd9, EXX())

    def step(self, cpu):
        cpu.EX_q_altq('B')
        cpu.EX_q_altq('C')
        cpu.EX_q_altq('D')
        cpu.EX_q_altq('E')
        cpu.EX_q_altq('H')
        cpu.EX_q_altq('L')


class EX_ref_SP_HL(Instruction):
    def __init__(self):
        self.fmt = "EX (SP), HL"
        self.size = 1

    @staticmethod
    def register(iset):
        iset.define_instr(0xe3, EXX())

    def step(self, cpu):
        tmp = cpu.GET_ref2_nn(cpu.SP())
        cpu.LD_ref2_nn_nn(cpu.SP(), cpu.GET_HL())
        cpu.LD_ii('HL', tmp)


class EX_ref_SP_index(Instruction):
    def __init__(self, index):
        assert_index(index)
        self.index = index
        self.fmt = "EX (SP), {0}".format(self.index)
        self.size = 2

    @staticmethod
    def register(iset):
        for dst, cdst in Instruction.index_code.items():
            iset.define_instr2(cdst, 0xe3, EX_ref_SP_index(dst))

    def step(self, cpu):
        tmp = cpu.GET_ref2_nn(cpu.SP())
        cpu.LD_ref2_nn_nn(cpu.SP(), cpu.GET_ii(self.index))
        cpu.LD_ii(self.index, tmp)
