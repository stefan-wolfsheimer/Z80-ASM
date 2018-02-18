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
from z80.assertions import assert_r
from z80.assertions import assert_index
from z80.assertions import assert_bcde


####################################################
#
# 8-bit load group
#
####################################################
class LD_r_r(Instruction):
    """
    LD r,r'
    """
    def __init__(self, r_dest, r_src):
        assert_r(r_dest)
        assert_r(r_src)
        self.r_dest = r_dest
        self.r_src = r_src
        self.size = 1

    @staticmethod
    def register(iset):
        # 01 rrr rrr
        offset = 0b01000000
        for dst, cdst in Instruction.r_code.items():
            for src, csrc in Instruction.r_code.items():
                iset.define_instr(offset + (cdst << 3) + csrc,
                                  LD_r_r(dst, src))

    def step(self, cpu):
        cpu.LD_r_n(cpu.GET_r(self.r_src))


class LD_r_n(Instruction):
    """
    LD r,n
    """
    def __init__(self, r_dst):
        assert_r(r_dst)
        self.r_dst = r_dst
        self.size = 2

    @staticmethod
    def register(iset):
        # 00 rrr 110
        offset = 0b00000110
        for dst, cdst in Instruction.r_code.items():
            iset.define_instr(offset + (cdst << 3), LD_r_n(dst))

    def step(self, cpu):
        cpu.LD_r_n(self.r_dst, cpu.GET_ref_PC_plus_d(1))


class LD_r_ref_HL(Instruction):
    """LD r, (HL)"""
    def __init__(self, r_dst):
        assert_r(r_dst)
        self.r_dst = r_dst
        self.size = 1

    @staticmethod
    def register(iset):
        # 01 rrr 110
        offset = 0b01000110
        for dst, cdst in Instruction.r_code.items():
            iset.define_instr(offset + (cdst << 3), LD_r_ref_HL(dst))

    def step(self, cpu):
        cpu.LD_r_n(self.r_dst, cpu.GET_ref_nn(cpu.GET_HL()))


class LD_r_ref_index_plus_d(Instruction):
    """LD r, (IX+d) or LD r, (IY+d)"""
    def __init__(self, r_dst, index):
        assert_r(r_dst)
        assert_index(index)
        self.r_dst = r_dst
        self.index = index
        self.size = 3

    @staticmethod
    def register(iset):
        # 01 rrr 110
        offset = 0b01000110
        for index, cindex in Instruction.index_code.items():
            for dst, cdst in Instruction.r_code.items():
                iset.define_instr2(cindex,
                                   offset + (cdst << 3),
                                   LD_r_ref_index_plus_d(dst, index))

    def step(self, cpu):
        d = cpu.GET_ref_PC_plus_d(2)
        cpu.LD_r_n(self.r_dst,
                   cpu.GET_ref_nn(cpu.GET_ii_plus_d(self.index, d)))


class LD_ref_HL_r(Instruction):
    """LD (HL), r"""
    def __init__(self, r_src):
        assert_r(r_src)
        self.r_src = r_src
        self.size = 1

    @staticmethod
    def register(iset):
        offset = 0b01110000
        for src, csrc in Instruction.r_code.items():
            iset.define_instr(offset + csrc,
                              LD_ref_HL_r(src))

    def step(self, cpu):
        cpu.LD_ref_nn_n(cpu.GET_HL(), cpu.GET_r(self.r_src))


class LD_ref_index_plus_d_r(Instruction):
    """LD (IX+d), r or LD (IY+d), r"""
    def __init__(self, index, r_src):
        assert_r(r_src)
        assert_index(index)
        self.r_src = r_src
        self.index = index
        self.size = 3

    @staticmethod
    def register(iset):
        # 01 110 rrr
        offset = 0b01110000
        for index, cindex in Instruction.index_code.items():
            for src, csrc in Instruction.r_code.items():
                iset.define_instr2(cindex,
                                   offset + csrc,
                                   LD_ref_index_plus_d_r(index, src))

    def step(self, cpu):
        d = cpu.GET_ref_PC_plus_d(2)
        cpu.LD_ref_nn_n(cpu.GET_ii_plus_d(self.index, d),
                        cpu.GET_r(self.r_src))


class LD_ref_HL_n(Instruction):
    """LD (HL), n"""
    def __init__(self):
        self.size = 2

    @staticmethod
    def register(iset):
        iset.define_instr(0x36, LD_ref_HL_n())

    def step(self, cpu):
        cpu.LD_ref_nn_n(cpu.GET_HL(), cpu.GET_ref_PC_plus_d(1))


class LD_ref_index_plus_d_n(Instruction):
    """LD (IX+d), n or LD (IY+d), n"""
    def __init__(self, index):
        assert_index(index)
        self.index = index
        self.size = 4

    @staticmethod
    def register(iset):
        for index, cindex in Instruction.index_code.items():
            iset.define_instr2(cindex, 0x36, LD_ref_index_plus_d_n(index))

    def step(self, cpu):
        d = cpu.GET_ref_PC_plus_d(2)
        n = cpu.GET_ref_PC_plus_d(2)
        cpu.LD_ref_nn_n(cpu.GET_ii_plus_d(self.index, d), n)


class LD_A_ref_bcde(Instruction):
    """LD A, (BC) or LD A, (DE)"""
    def __init__(self, ref_src):
        assert_bcde(ref_src)
        self.ref_src = ref_src
        self.size = 1

    @staticmethod
    def register(iset):
        iset.define_instr(0x0a, LD_A_ref_bcde('BC'))
        iset.define_instr(0x1a, LD_A_ref_bcde('DE'))

    def step(self, cpu):
        cpu.LD_A_n(cpu.GET_ref_nn(cpu.GET_ii(self.ref_src)))


class LD_A_ref_nn(Instruction):
    """LD A, (nn)"""
    def __init__(self):
        self.size = 3

    @staticmethod
    def register(iset):
        iset.define_instr(0x3a, LD_A_ref_nn())

    def step(self, cpu):
        nn = (cpu.GET_PC_plus_d(2) << 8) + cpu.GET_PC_plus_d(1)
        cpu.LD_A_n(cpu.GET_ref_nn(nn))


class LD_ref_bcde_A(Instruction):
    """LD (BC),A or LD (DE),A"""
    def __init__(self, ref_dst):
        assert_bcde(ref_dst)
        self.ref_dst = ref_dst
        self.size = 1

    @staticmethod
    def register(iset):
        iset.define_instr(0x02, LD_ref_bcde_A('BC'))
        iset.define_instr(0x12, LD_ref_bcde_A('DE'))

    def step(self, cpu):
        cpu.LD_ref_nn_n(cpu.GET_ii(self.ref_dst), cpu.GET_A())


class LD_ref_nn_A(Instruction):
    def __init__(self):
        self.size = 3

    @staticmethod
    def register(iset):
        iset.define_instr(0x32, LD_ref_nn_A())

    def step(self, cpu):
        nn = (cpu.GET_PC_plus_d(2) << 8) + cpu.GET_PC_plus_d(1)
        cpu.LD_ref_nn_n(nn, cpu.GET_A())


class LD_A_I(Instruction):
    def __init__(self):
        self.size = 2

    @staticmethod
    def register(iset):
        iset.define_instr2(0xed, 0x57, LD_A_I())

    def step(self, cpu):
        cpu.LD_A_n(cpu.GET_I())


class LD_A_R(Instruction):
    def __init__(self):
        self.size = 2

    @staticmethod
    def register(iset):
        iset.define_instr2(0xed, 0x5f, LD_A_R())

    def step(self, cpu):
        cpu.LD_A_n(cpu.GET_R())


class LD_I_A(Instruction):
    def __init__(self):
        self.size = 2

    @staticmethod
    def register(iset):
        iset.define_instr2(0xed, 0x47, LD_I_A())

    def step(self, cpu):
        cpu.LD_I_n(cpu.GET_A())


class LD_R_A(Instruction):
    def __init__(self):
        self.size = 2

    @staticmethod
    def register(iset):
        iset.define_instr2(0xed, 0x4f, LD_R_A())

    def step(self, cpu):
        cpu.LD_R_n(cpu.GET_A())
