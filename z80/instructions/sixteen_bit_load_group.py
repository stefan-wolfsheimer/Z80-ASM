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
from z80.assertions import assert_dd
from z80.assertions import assert_index
from z80.assertions import assert_qq


####################################################
#
# 16-bit load group
#
####################################################
class LD_dd_nn(Instruction):
    """ LD dd, nn"""
    def __init__(self, dd_dst):
        assert_dd(dd_dst)
        self.dd_dst = dd_dst
        self.fmt = "LD {0}, nn".format(self.dd_dst)
        self.size = 3

    @staticmethod
    def register(iset):
        # 00 dd 0001
        offset = 0b00000001
        for dst, cdst in Instruction.dd_code.items():
            iset.define_instr(offset + (cdst << 4), LD_dd_nn(dst))

    def step(self, cpu):
        cpu.LD_dd_nn(self.r_high_dst, cpu.GET_ref2_PC_plus_d(1))


class LD_index_nn(Instruction):
    """ LD IX, nn or LD IY, nn"""
    def __init__(self, index_dst):
        assert_index(index_dst)
        self.index_dst = index_dst
        self.fmt = "LD {0}, nn".format(self.index_dst)
        self.size = 4

    @staticmethod
    def register(iset):
        for dst, cdst in Instruction.index_code.items():
            iset.define_instr2(cdst, 0x21, LD_index_nn(dst))

    def step(self, cpu):
        cpu.LD_index_nn(self.index_dst, cpu.GET_ref2_PC_plus_d(1))


class LD_HL_ref_nn(Instruction):
    """ LD HL, (nn)"""
    def __init__(self):
        self.fmt = "LD HL, nn"
        self.size = 3

    @staticmethod
    def register(iset):
        iset.define_instr(0x2a, LD_HL_ref_nn())

    def step(self, cpu):
        cpu.LD_dd_nn('HL', cpu.GET_ref2_PC_plus_d(1))


class LD_dd_ref_nn(Instruction):
    """ LD dd, (nn)"""
    def __init__(self, dd_dst):
        assert_dd(dd_dst)
        self.dd_dst = dd_dst
        self.fmt = "LD {0}, (nn)".format(self.dd_dst)
        self.size = 4

    @staticmethod
    def register(iset):
        for dst, cdst in Instruction.dd_code.items():
            offset = 0b01001011
            iset.define_instr2(0xed, (cdst << 4) + offset, LD_dd_ref_nn(dst))

    def step(self, cpu):
        cpu.LD_dd_nn(self.dd_dst, cpu.GET_ref2_PC_plus_d(2))


class LD_index_ref_nn(Instruction):
    """ LD IX, (nn) / LD IY, (nn)"""
    def __init__(self, index_dst):
        assert_index(index_dst)
        self.index_dst = index_dst
        self.fmt = "LD {0}, (nn)".format(self.index_dst)
        self.size = 4

    @staticmethod
    def register(iset):
        for dst, cdst in Instruction.index_code.items():
            iset.define_instr2(cdst, 0x2a, LD_index_ref_nn(dst))

    def step(self, cpu):
        cpu.LD_index_nn(self.index_dest, cpu.GET_ref2_PC_plus_d(2))


class LD_ref_nn_HL(Instruction):
    """ LD (nn), HL"""
    def __init__(self):
        self.fmt = "LD (nn), HL"
        self.size = 3

    @staticmethod
    def register(iset):
        iset.define_instr(0x22, LD_ref_nn_HL())

    def step(self, cpu):
        cpu.LD_ref_nn_nn(cpu.GET_ref2_PC_plus_d(1), cpu.GET_HL())


class LD_ref_nn_dd(Instruction):
    """ LD (nn), dd"""
    def __init__(self, dd_src):
        assert_dd(dd_src)
        self.dd_src = dd_src
        self.fmt = "LD (nn), {0}".format(self.dd_src)
        self.size = 4

    @staticmethod
    def register(iset):
        for dst, cdst in Instruction.dd_code.items():
            offset = 0b01000011
            iset.define_instr2(0xed, (cdst << 4) + offset, LD_ref_nn_dd(dst))

    def step(self, cpu):
        cpu.LD_ref_nn_nn(cpu.GET_ref2_PC_plus_d(2), cpu.GET_ii(self.dd_src))


class LD_ref_nn_index(Instruction):
    """ LD (nn), IX or LD (nn), IY"""
    def __init__(self, index_src):
        assert_index(index_src)
        self.index_src = index_src
        self.fmt = "LD (nn), {0}".format(self.index_src)
        self.size = 4

    @staticmethod
    def register(iset):
        for dst, cdst in Instruction.index_code.items():
            iset.define_instr2(cdst, 0x22, LD_ref_nn_index(dst))

    def step(self, cpu):
        cpu.LD_ref_nn_nn(cpu.GET_ref2_PC_plus_d(2), cpu.GET_ii(self.index_src))


class LD_SP_HL(Instruction):
    """ LD SP, HL"""
    def __init__(self):
        self.fmt = "LD SP, HL"
        self.size = 1

    @staticmethod
    def register(iset):
        iset.define_instr(0xf9, LD_SP_HL())

    def step(self, cpu):
        cpu.LD_SP_nn(cpu.GET_HL())


class LD_SP_index(Instruction):
    """ LD SP, IX / LD SP, IY"""
    def __init__(self, src_index):
        assert_index(src_index)
        self.src_index = src_index
        self.fmt = "LD SP, {0}".format(self.src_index)
        self.size = 2

    @staticmethod
    def register(iset):
        for dst, cdst in Instruction.index_code.items():
            iset.define_instr2(cdst, 0xf9, LD_SP_index(dst))

    def step(self, cpu):
        cpu.LD_SP_nn(cpu.GET_ii(self.src_index))


class PUSH_qq(Instruction):
    """ PUSH qq"""
    def __init__(self, qq):
        assert_qq(qq)
        self.qq = qq
        self.fmt = "PUSH {0}".format(self.qq)
        self.size = 1

    @staticmethod
    def register(iset):
        # 11 qq 0100
        offset = 0b11000101
        for dst, cdst in Instruction.qq_code.items():
            iset.define_instr(offset + (cdst << 4), PUSH_qq(dst))

    def step(self, cpu):
        cpu.DEC_SP(2)
        cpu.LD_ref_nn_nn(cpu.GET_SP(), cpu.GET_ii(self.qq))


class PUSH_index(object):
    """ PUSH IX / PUSH IY"""
    def __init__(self, index):
        assert_index(index)
        self.index = index
        self.fmt = "PUSH {0}".format(self.index)
        self.size = 2

    @staticmethod
    def register(iset):
        for dst, cdst in Instruction.index_code.items():
            iset.define_instr2(cdst, 0xe5, PUSH_index(dst))

    def step(self, cpu):
        cpu.DEC_SP(2)
        cpu.LD_ref_nn_nn(cpu.GET_SP(), cpu.GET_ii(self.index))


class POP_qq(object):
    """ POP qq"""
    def __init__(self, qq):
        assert_qq(qq)
        self.qq = qq
        self.fmt = "POP {0}".format(self.qq)
        self.size = 1

    @staticmethod
    def register(iset):
        # 11 qq 0001
        offset = 0b11000001
        for dst, cdst in Instruction.qq_code.items():
            iset.define_instr(offset + (cdst << 4), POP_qq(dst))

    def step(self, cpu):
        cpu.LD_ii_nn(self.qq, cpu.GET_ref_nn(cpu.GET_SP()))
        cpu.INC_SP(2)


class POP_index(object):
    """ POP IX / POP IY"""
    def __init__(self, index):
        assert_index(index)
        self.index = index
        self.fmt = "POP {0}".format(self.index)
        self.size = 2

    @staticmethod
    def register(iset):
        for dst, cdst in Instruction.index_code.items():
            iset.define_instr2(cdst, 0xe1, POP_index(dst))

    def step(self, cpu):
        cpu.LD_ii_nn(self.qq, cpu.GET_ref_nn(cpu.GET_SP()))
        cpu.INC_SP(2)
