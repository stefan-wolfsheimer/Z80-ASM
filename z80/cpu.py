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

from z80.assertions import assert_n
from z80.assertions import assert_nn
from z80.assertions import assert_d
from z80.assertions import assert_r
from z80.assertions import assert_ii
from z80.instructions import InstructionSet


class CPU(object):
    MEMSIZE = 0x10000

    def __init__(self):
        self.B = 0x00
        self.C = 0x00
        self.D = 0x00
        self.E = 0x00
        self.H = 0x00
        self.L = 0x00
        self.A = 0x00
        self.F = 0x00
        self.I = 0x00
        self.R = 0x00
        self.IX = 0x0000
        self.IY = 0x0000
        self.PC = 0x0000
        self.SP = 0x0000
        self.mem = bytearray(CPU.MEMSIZE)
        self.instr_set = InstructionSet()

    # 8 bit load #
    def LD_r_n(self, r_dest, n):
        """ LD r, n"""
        assert_r(r_dest)
        assert_n(n)
        setattr(self, r_dest, n)

    def LD_A_n(self, n):
        """ LD A,n """
        assert_n(n)
        self.A = n

    def LD_F_n(self, n):
        """ LD F, n"""
        assert_n(n)
        self.F = n

    def LD_I_n(self, n):
        """ LD I, n"""
        assert_n(n)
        self.I = n

    def LD_R_n(self, n):
        """ LD R, n"""
        assert_n(n)
        self.R = n

    def LD_ref_nn_n(self, nn, n):
        """ LD (nn), n"""
        assert_nn(nn)
        assert_n(n)
        self.mem[nn] = n

    # 16 bit load #
    def LD_PC_nn(self, nn):
        """ LD PC, nn"""
        assert_nn(nn)
        self.PC = nn

    def LD_SP_nn(self, nn):
        """ LD SP, nn"""
        assert_nn(nn)
        self.SP = nn

    def LD_IX_nn(self, nn):
        """ LD IX, nn"""
        assert_nn(nn)
        self.IX = nn

    def LD_IY_nn(self, nn):
        """ LD IY, nn"""
        assert_nn(nn)
        self.IY = nn

    # 8 bit getter #
    def GET_r(self, r):
        """B,C,D,E,H,L or A"""
        assert_r(r)
        return getattr(self, r)

    def GET_A(self):
        return self.A

    def GET_F(self):
        return self.F

    def GET_I(self):
        return self.I

    def GET_R(self):
        return self.R

    def GET_ref_nn(self, nn):
        """(nn)"""
        assert_nn(nn)
        return self.mem[nn]

    def GET_ref_PC_plus_d(self, d):
        """ eq. to self.GET_ref_nn(self.GET_ref_ii_plus_d('PC', 1)))"""
        return self.mm[self.GET_ii_plus_d('PC', d)]

    # 16 bit getter #
    def GET_PC(self):
        return self.PC

    def GET_SP(self):
        return self.SP

    def GET_BC(self):
        return (self.B << 8) + self.C

    def GET_DE(self):
        return (self.D << 8) + self.E

    def GET_HL(self):
        return (self.H << 8) + self.L

    def GET_AF(self):
        return (self.A << 8) + self.F

    def GET_IX(self):
        return self.IX

    def GET_IY(self):
        return self.IY

    def GET_IR(self):
        return (self.I << 8) + self.R

    def GET_ii(self, ii):
        assert_ii(ii)
        getter = getattr(self, 'GET_' + ii)
        return getter()

    def GET_ii_plus_d(self, ii, d):
        """ ii + d """
        assert_d(d)
        nn = self.GET_ii(ii)
        return (nn + d) % CPU.MEMSIZE

    # arithmetic
    def INC_PC(self, n=1):
        """ PC <- PC + n """
        assert_n(n)
        self.PC = (self.PC + n) % CPU.MEMSIZE
