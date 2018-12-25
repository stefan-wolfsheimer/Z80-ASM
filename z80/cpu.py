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

from assertions import assert_n
from assertions import assert_nn
from assertions import assert_d
from assertions import assert_r
from assertions import assert_b
from assertions import assert_ii
from assertions import assert_dd
from assertions import assert_rr
from assertions import assert_ss
from assertions import assert_qq
from assertions import assert_pp

from util import parity
from instruction_group import InstructionGroup
from instruction_group import InstructionDecor as I
from register import RegisterSet
from register import RegisterPlusOffset
from register import MEMSIZE
from register import HL
from register import BC
from register import DE


ALL_INSTRUCTIONS = InstructionGroup("all instructions")
EIGHT_BIT_LOAD_GROUP = InstructionGroup("8 bit load group",
                                        ALL_INSTRUCTIONS)
SIXTEEN_BIT_LOAD_GROUP = InstructionGroup("16 bit load group",
                                          ALL_INSTRUCTIONS)
EXCHANGE_GROUP = InstructionGroup("exchange group",
                                  ALL_INSTRUCTIONS)
BLOCK_TRANSFER_GROUP = InstructionGroup("block transfer group",
                                        ALL_INSTRUCTIONS)
SEARCH_GROUP = InstructionGroup("search group",
                                ALL_INSTRUCTIONS)
EIGHT_BIT_ARITHMETIC_GROUP = InstructionGroup("8 bit arithmetic group",
                                              ALL_INSTRUCTIONS)
GENERAL_PURPOSE_GROUP = InstructionGroup("general purpose group",
                                         ALL_INSTRUCTIONS)
SIXTEEN_BIT_ARITHMETIC_GROUP = InstructionGroup("16 bit arithmetic group",
                                                ALL_INSTRUCTIONS)
ROTATE_AND_SHIFT_GROUP = InstructionGroup("rotate and shift group",
                                          ALL_INSTRUCTIONS)

BIT_SET_RESET_TEST_GROUP = InstructionGroup("bit set reset test group",
                                            ALL_INSTRUCTIONS)


class CPU(object):
    def __init__(self):
        self.reg = RegisterSet()

    def __getitem__(self, key):
        return self.reg[key]

    def __setitem__(self, key, value):
        self.reg[key] = value

    def get16(self, key):
        return self.reg.get16(key)

    def set16(self, key, value):
        self.reg.set16(key, value)

    def fetch(self):
        return ALL_INSTRUCTIONS.fetch(self)

    def instr_cycle(self):
        instr = self.instr_set.fetch(self)
        instr.step(self)
        self.INC_PC(instr.size)

    # ################ #
    # 8 bit load group #
    # ################ #
    @I(EIGHT_BIT_LOAD_GROUP, "01{0}{1}", expand=['r', 'r'])
    def LD_r_r(self, r1, r2):
        """ {0} <- {1} """
        assert_r(r1)
        assert_r(r2)
        self[r1] = self[r2]

    @I(EIGHT_BIT_LOAD_GROUP, ["00{0}110", "n"], expand=['r'])
    def LD_r_n(self, r, n):
        """ {0} <- {1}"""
        assert_r(r)
        assert_n(n)
        self[r] = n

    @I(EIGHT_BIT_LOAD_GROUP, "01{0}110", expand=['r'])
    def LD_r__HL_(self, r):
        """ {0} <- (HL) """
        assert_r(r)
        self[r] = self[HL()]

    @I(EIGHT_BIT_LOAD_GROUP, ["11{1}101", "01{0}110", "d"], expand=['r', 'ii'])
    def LD_r__ii_d_(self, r, ii, d):
        """ {0} <- ({1} + d) """
        assert_r(r)
        assert_ii(ii)
        assert_d(d)
        self[r] = self[RegisterPlusOffset(ii, d)]

    @I(EIGHT_BIT_LOAD_GROUP, "01110{0}", expand=['r'])
    def LD__HL__r(self, r):
        """ (HL) <- {0} """
        assert_r(r)
        self[HL()] = self[r]

    @I(EIGHT_BIT_LOAD_GROUP, [0x36, "n"])  # 00 110 110
    def LD__HL__n(self, n):
        """ (HL) <- n """
        assert_n(n)
        self[HL()] = n

    @I(EIGHT_BIT_LOAD_GROUP, ["11{0}101", "01110{1}", "d"], expand=['ii', 'r'])
    def LD__ii_d__r(self, ii, r, d):
        assert_ii(ii)
        assert_d(d)
        assert_r(r)
        self[RegisterPlusOffset(ii, d)] = self[r]

    @I(EIGHT_BIT_LOAD_GROUP, ["11{0}101", 0x36, "d", "n"], expand=['ii'])
    def LD__ii_d__n(self, ii, d, n):
        assert_ii(ii)
        assert_n(n)
        assert_d(d)
        self[RegisterPlusOffset(ii, d)] = n

    @I(EIGHT_BIT_LOAD_GROUP, [0x0a])
    def LD_A__BC_(self):
        """ A <- (BC) """
        self['A'] = self[BC()]

    @I(EIGHT_BIT_LOAD_GROUP, [0x1a])
    def LD_A__DE_(self):
        """ A <- (DE) """
        self['A'] = self[DE()]

    # todo: 16 bit values in opcode
    @I(EIGHT_BIT_LOAD_GROUP, [0x3a, "nn"])
    def LD_A__nn_(self, nn):
        """ A <- (nn) """
        assert_nn(nn)
        self['A'] = self[nn]

    @I(EIGHT_BIT_LOAD_GROUP, [0x02])
    def LD__BC__A(self):
        """ (BC) <- A """
        self[BC()] = self['A']

    @I(EIGHT_BIT_LOAD_GROUP, [0x12])
    def LD__DE__A(self):
        """ (DE) <- A """
        self[DE()] = self['A']

    @I(EIGHT_BIT_LOAD_GROUP, [0x32, "nn"])
    def LD__nn__A(self, nn):
        """ (nn) <- A """
        assert_nn(nn)
        self[nn] = self['A']

    @I(EIGHT_BIT_LOAD_GROUP, [0xed, 0x57])
    def LD_A_I(self):
        """ A <- I """
        self['A'] = self['I']

    @I(EIGHT_BIT_LOAD_GROUP, [0xed, 0x5f])
    def LD_A_R(self):
        """ A <- R """
        self['A'] = self['R']

    @I(EIGHT_BIT_LOAD_GROUP, [0xed, 0x47])
    def LD_I_A(self):
        """ I <- A """
        self['I'] = self['A']

    @I(EIGHT_BIT_LOAD_GROUP, [0xed, 0x4f])
    def LD_R_A(self):
        """ R <- A """
        self['R'] = self['A']

    # ##################
    # 16 bit load group
    # ##################
    @I(SIXTEEN_BIT_LOAD_GROUP, ["00{0}0001", "nn"], expand=['dd'])
    def LD_dd_nn(self, dd, nn):
        """ {0} <- nn """
        assert_dd(dd)
        assert_nn(nn)
        self[dd] = nn

    @I(SIXTEEN_BIT_LOAD_GROUP, ["11{0}101", 0x21, "nn"], expand=['ii'])
    def LD_ii_nn(self, ii, nn):
        """ {0} <- nn """
        assert_ii(ii)
        assert_nn(nn)
        self[ii] = nn

    @I(SIXTEEN_BIT_LOAD_GROUP, [0x2a, "nn"])
    def LD_HL__nn_(self, nn):
        """ HL <- (nn) """
        assert_nn(nn)
        self['HL'] = self.get16(nn)

    @I(SIXTEEN_BIT_LOAD_GROUP, [0xed, "01{0}1011", "nn"], expand=['dd'])
    def LD_dd__nn_(self, dd, nn):
        """ dd <- (nn) """
        assert_nn(nn)
        assert_dd(dd)
        self[dd] = self.get16(nn)

    @I(SIXTEEN_BIT_LOAD_GROUP, ["11{0}101", 0x2a, "nn"], expand=['ii'])
    def LD_ii__nn_(self, ii, nn):
        """ {0} <- (nn) """
        assert_ii(ii)
        assert_nn(nn)
        self[ii] = self.get16(nn)

    @I(SIXTEEN_BIT_LOAD_GROUP, [0x22, "nn"])
    def LD__nn__HL(self, nn):
        """ (nn) <- HL, """
        assert_nn(nn)
        self.set16(nn, self['HL'])

    @I(SIXTEEN_BIT_LOAD_GROUP, [0xed, "01{0}0011", "nl", "nh"], expand=['dd'])
    def LD__nn__dd(self, nn, dd):
        """ (nn) <- dd """
        assert_nn(nn)
        assert_dd(dd)
        self.set16(nn, self[dd])

    @I(SIXTEEN_BIT_LOAD_GROUP, ["11{0}101", 0x22, "nn"], expand=['ii'])
    def LD__nn__ii(self, nn, ii):
        """ (nn) <- {0} """
        assert_ii(ii)
        assert_nn(nn)
        self.set16(nn, self[ii])

    @I(SIXTEEN_BIT_LOAD_GROUP, [0xf9])
    def LD_SP_HL(self):
        """ SP <- HL """
        self['SP'] = self['HL']

    @I(SIXTEEN_BIT_LOAD_GROUP, ["11{0}101", 0xf9], expand=['ii'])
    def LD_SP_ii(self, ii):
        """ SP <- {0} """
        assert_ii(ii)
        self['SP'] = self[ii]

    @I(SIXTEEN_BIT_LOAD_GROUP, ["11{0}0101"], expand=['qq'])
    def PUSH_qq(self, qq):
        """ (SP-2) <- qq,
            SP <- SP-2 """
        assert_qq(qq)
        self.DEC_ss('SP', 2)
        self.set16(self['SP'], self[qq])

    @I(SIXTEEN_BIT_LOAD_GROUP, ["11{0}101", 0xe5], expand=['ii'])
    def PUSH_ii(self, ii):
        """ (SP-2) <- {0},
            SP <- SP-2 """
        assert_ii(ii)
        self.DEC_ss('SP', 2)
        self.set16(self['SP'], self[ii])

    @I(SIXTEEN_BIT_LOAD_GROUP, ["11{0}0001"], expand=['qq'])
    def POP_qq(self, qq):
        """ qq <- (SP),
            SP <- SP+2 """
        self[qq] = self.get16(self['SP'])
        self.INC_ss('SP', 2)

    @I(SIXTEEN_BIT_LOAD_GROUP, ["11{0}101", 0xe1], expand=['ii'])
    def POP_ii(self, ii):
        """ {0} <- (SP)
            SP <- SP+2 """
        assert_ii(ii)
        self[ii] = self.get16(self['SP'])
        self.INC_ss('SP', 2)

    # ##################
    # exchange
    # ##################
    @I(EXCHANGE_GROUP, [0xeb])
    def EX_DE_HL(self):
        """ DE <-> HL """
        tmp = self['DE']
        self['DE'] = self['HL']
        self['HL'] = tmp

    @I(EXCHANGE_GROUP, [0x08], assembler=["EX", "AF", "AF'"])
    def EX_AF_alt_AF(self):
        """ AF <-> AF' """
        self.reg.ex_q_alt_q('A')
        self.reg.ex_q_alt_q('F')

    @I(EXCHANGE_GROUP, [0xd9])
    def EXX(self):
        self.reg.ex_q_alt_q('B')
        self.reg.ex_q_alt_q('C')
        self.reg.ex_q_alt_q('D')
        self.reg.ex_q_alt_q('E')
        self.reg.ex_q_alt_q('H')
        self.reg.ex_q_alt_q('L')

    @I(EXCHANGE_GROUP, [0xe3])
    def EX__SP__HL(self):
        """ H <-> (SP+1)
            L <-> (SP) """
        tmp = self.get16(self['SP'])
        self.set16(self['SP'], self['HL'])
        self['HL'] = tmp

    @I(EXCHANGE_GROUP, ["11{0}101", 0xe3], expand=['ii'])
    def EX__SP__ii(self, ii):
        """ {0}_h <-> (SP+1)
            {0}_l <-> (SP) """
        assert_ii(ii)
        tmp = self.get16(self['SP'])
        self.set16(self['SP'], self[ii])
        self[ii] = tmp

    # ##############
    # block transfer
    # ##############
    # todo: make t-states dynamic, depending on the result
    # T-states for LDIR and LDDR: if BC = 0: 16
    @I(BLOCK_TRANSFER_GROUP, [0xed, 0xa0], tstates=16)
    def LDI(self):
        """ (DE) <- (HL)
            DE <- DE + 1
            HL <- HL + 1
            BC <- BC - 1 """
        self[self['DE']] = self[self['HL']]
        self.INC_ii('DE')
        self.INC_ii('HL')
        self.DEC_ii('BC')
        self['H'] = 0
        self['N'] = 0
        self['V'] = 1 if self['BC'] == 1 else 0

    @I(BLOCK_TRANSFER_GROUP, [0xed, 0xb0], tstates=21)
    def LDIR(self):
        """ (DE) <- (HL)
            DE <- DE + 1
            HL <- HL + 1
            BC <- BC - 1
            WHILE BC != 0 """
        self.LDI()
        if self['BC'] != 0x0000:
            self.DEC_PC(2)

    @I(BLOCK_TRANSFER_GROUP, [0xed, 0xa8], tstates=16)
    def LDD(self):
        """ (DE) <- (HL)
            DE <- DE - 1
            HL <- HL - 1
            BC <- BC - 1 """
        self[self['DE']] = self[self['HL']]
        self.DEC_ii('DE')
        self.DEC_ii('HL')
        self.DEC_ii('BC')
        self['H'] = 0
        self['N'] = 0
        self['V'] = 1 if self['BC'] == 1 else 0

    @I(BLOCK_TRANSFER_GROUP, [0xed, 0xb8], tstates=21)
    def LDDR(self):
        """ (DE) <- (HL)
            DE <- DE - 1
            HL <- HL - 1
            BC <- BC - 1
            WHILE BC != 0 """
        self.LDD()
        if self['BC'] != 0x0000:
            self.DEC_PC(2)

    # ############
    # Search group
    # ############
    @I(SEARCH_GROUP, [0xed, 0xa1], tstates=16)
    def CPI(self):
        """ A - (HL)
            HL <- HL + 1
            BC <- BC - 1 """
        self['A'] = self[self['HL']]
        self['V'] = (self['BC'] != 0x00001)
        self.INC_ii('HL')
        self.DEC_ii('BC')

    @I(SEARCH_GROUP, [0xed, 0xb1], tstates=21)
    def CPIR(self):
        """ A - (HL)
            HL <- HL + 1
            BC <- BC - 1 """
        self.CPI()
        if self['BC'] != 0x0000:
            self.DEC_PC(2)

    @I(SEARCH_GROUP, [0xed, 0xa9], tstates=16)
    def CPD(self):
        """ A - (HL)
            HL <- HL - 1
            BC <- BC - 1 """
        self['A'] = self[self['HL']]
        self['V'] = (self.GET_BC() != 0x00001)
        self.DEC_ii('HL')
        self.DEC_ii('BC')

    @I(SEARCH_GROUP, [0xed, 0xb9], tstates=16)
    def CPDR(self):
        """ A - (HL)
            HL <- HL - 1
            BC <- BC - 1 """
        self.CPD()
        if self['BC'] != 0x0000:
            self.DEC_PC(2)

    # ################
    # 8-bit arithmetic
    # ################
    @I(EIGHT_BIT_ARITHMETIC_GROUP, [0xc6, 'n'], tstates=7)
    def ADD_A_n(self, n, carry=0):
        """ A <- A + n """
        assert_n(n)
        a = self['A']
        res = a + n + carry
        res_modulo = res % 0x100
        HM = 0b00001111
        MSB = 0b10000000
        overflow = (a & MSB) == (n & MSB) and (res_modulo & MSB) != (a & MSB)
        self['S'] = (res_modulo & 0b10000000)
        self['Z'] = (res_modulo == 0x00)
        self['5'] = (res_modulo & 0b00100000)
        # todo check H flag
        self['H'] = ((a & HM) + (n & HM) + carry > HM)
        self['3'] = (res_modulo & 0b00001000)
        self['V'] = overflow
        self['N'] = False
        self['C'] = (res > 0x100)
        self['A'] = res_modulo

    @I(EIGHT_BIT_ARITHMETIC_GROUP, ['10000{0}'], tstates=4, expand=['r'])
    def ADD_A_r(self, r):
        """ A <- A + {0} """
        assert_r(r)
        self.ADD_A_n(self[r])

    @I(EIGHT_BIT_ARITHMETIC_GROUP, [0x86], tstates=7)
    def ADD_A__HL_(self):
        """ A <- A + (HL) """
        self.ADD_A_n(self[self['HL']])

    @I(EIGHT_BIT_ARITHMETIC_GROUP, ['11{0}101', 0x86, 'd'], tstates=19,
       expand=['ii'])
    def ADD_A__ii_d_(self, ii, d):
        """ A <- A + ({0}+d) """
        assert_ii(ii)
        assert_d(d)
        self.ADD_A_n(self[RegisterPlusOffset(ii, d)])

    @I(EIGHT_BIT_ARITHMETIC_GROUP, [0xce, 'n'], tstates=7)
    def ADC_A_n(self, n):
        """ A <- A + n """
        assert_n(n)
        self.ADD_A_n(n, carry=self['C'])

    @I(EIGHT_BIT_ARITHMETIC_GROUP, ['10001{0}'], tstates=4, expand=['r'])
    def ADC_A_r(self, r):
        """ A <- A + {0} + CY """
        assert_r(r)
        self.ADC_A_n(self[r])

    @I(EIGHT_BIT_ARITHMETIC_GROUP, [0x8e], tstates=7)
    def ADC_A__HL_(self):
        """ A <- A + (HL) """
        self.ADC_A_n(self[self['HL']])

    @I(EIGHT_BIT_ARITHMETIC_GROUP, ['11{0}101', 0x8e, 'd'], tstates=19,
       expand=['ii'])
    def ADC_A__ii_d_(self, ii, d):
        """ A <- A + ({0}+d) """
        assert_ii(ii)
        assert_d(d)
        self.ADC_A_n(self[RegisterPlusOffset(ii, d)])

    @I(EIGHT_BIT_ARITHMETIC_GROUP, [0xd6, 'n'], tstates=7)
    def SUB_A_n(self, n, carry=0):
        """ A <- A - n """
        assert_n(n)
        self.ADD_A_n((0x100 - n) % 0x100, carry)

    @I(EIGHT_BIT_ARITHMETIC_GROUP, ['10010{0}'], tstates=4, expand=['r'])
    def SUB_A_r(self, r):
        """ A <- A - {0} """
        assert_r(r)
        self.SUB_A_n(self['r'])

    @I(EIGHT_BIT_ARITHMETIC_GROUP, [0x96], tstates=7)
    def SUB_A__HL_(self):
        """ A <- A - (HL) """
        self.SUB_A_n(self[self['HL']])

    @I(EIGHT_BIT_ARITHMETIC_GROUP, ['11{0}101', 0x96, 'd'], tstates=19,
       expand=['ii'])
    def SUB_A__ii_d_(self, ii, d):
        """ A <- A - ({0}+d) """
        assert_ii(ii)
        assert_d(d)
        self.SUB_A_n(self[RegisterPlusOffset(ii, d)])

    @I(EIGHT_BIT_ARITHMETIC_GROUP, [0xde, 'n'], tstates=7)
    def SBC_A_n(self, n):
        """ A <- A - n - CY """
        assert_n(n)
        self.SUB_A_n(n, carry=1)

    @I(EIGHT_BIT_ARITHMETIC_GROUP, ['10011{0}'], tstates=4, expand=['r'])
    def SBC_A_r(self, r):
        """ A <- A - {0} - CY """
        assert_r(r)
        self.SBC_A_n(self[r])

    @I(EIGHT_BIT_ARITHMETIC_GROUP, [0x9e], tstates=7)
    def SBC_A__HL_(self):
        """ A <- A - (HL) - CY """
        self.SBC_n(self[self['HL']])

    @I(EIGHT_BIT_ARITHMETIC_GROUP, ['11{0}101', 0x9e, 'd'], tstates=19,
       expand=['ii'])
    def SBC_A__ii_d_(self, ii, d):
        """ A <- A - ({0}+d) - CY"""
        self.SBC_A_n(self[RegisterPlusOffset(ii, d)])

    @I(EIGHT_BIT_ARITHMETIC_GROUP, [0xe6, 'n'], tstates=7)
    def AND_A_n(self, n):
        """ A <- A AND n """
        assert_n(n)
        a = self['A']
        a &= n
        self['S'] = (a & 0b10000000)
        self['Z'] = (a == 0x00)
        self['H'] = True
        self['P'] = parity(a)
        self['N'] = False
        self['C'] = False
        self['A'] = a

    @I(EIGHT_BIT_ARITHMETIC_GROUP, ['10100{0}'], tstates=4, expand=['r'])
    def AND_A_r(self, r):
        """ A <- A AND {0} """
        assert_r(r)
        self.AND_A_n(self[r])

    @I(EIGHT_BIT_ARITHMETIC_GROUP, [0xa6], tstates=7)
    def AND_A__HL_(self):
        """ A <- A AND (HL) """
        self.AND_A_n(self[self['HL']])

    @I(EIGHT_BIT_ARITHMETIC_GROUP, ['11{0}101', 0xa6, 'd'], tstates=19,
       expand=['ii'])
    def AND_A__ii_d_(self, ii, d):
        """ A <- A AND ({0}+d) """
        assert_ii(ii)
        assert_d(d)
        self.AND_A_n(self[RegisterPlusOffset(ii, d)])

    @I(EIGHT_BIT_ARITHMETIC_GROUP, [0xf6, 'n'], tstates=7)
    def OR_A_n(self, n):
        """ A <- A OR n """
        assert_n(n)
        a = self['A']
        a |= n
        self['S'] = (a & 0b10000000)
        self['Z'] = (a == 0x00)
        self['H'] = True
        self['P'] = parity(a)
        self['N'] = False
        self['C'] = False
        self['A'] = a

    @I(EIGHT_BIT_ARITHMETIC_GROUP, ['10110{0}'], tstates=4, expand=['r'])
    def OR_A_r(self, r):
        """ A <- A OR {0} """
        assert_r(r)
        self.OR_A_n(self[r])

    @I(EIGHT_BIT_ARITHMETIC_GROUP, [0xb6], tstates=7)
    def OR_A__HL_(self):
        """ A <- A OR (HL) """
        self.OR_A_n(self[self['HL']])

    @I(EIGHT_BIT_ARITHMETIC_GROUP, ['11{0}101', 0xb6, 'd'], tstates=19,
       expand=['ii'])
    def OR_A__ii_d_(self, ii, d):
        """ A <- A OR ({0}+d) """
        assert_ii(ii)
        assert_d(d)
        self.OR_A_n(self[RegisterPlusOffset(ii, d)])

    @I(EIGHT_BIT_ARITHMETIC_GROUP, [0xee, 'n'], tstates=7)
    def XOR_A_n(self, n):
        """ A <- A XOR n """
        assert_n(n)
        a = self['A']
        a ^= n
        self['S'] = (a & 0b10000000)
        self['Z'] = (a == 0x00)
        self['H'] = True
        self['P'] = parity(a)
        self['N'] = False
        self['C'] = False
        self['A'] = a

    @I(EIGHT_BIT_ARITHMETIC_GROUP, ['10101{0}'], tstates=4, expand=['r'])
    def XOR_A_r(self, r):
        """ A <- A XOR {0} """
        assert_r(r)
        self.XOR_A_n(self[r])

    @I(EIGHT_BIT_ARITHMETIC_GROUP, [0xae], tstates=7)
    def XOR_A__HL_(self):
        """ A <- A XOR (HL) """
        self.XOR_A_n(self[self['HL']])

    @I(EIGHT_BIT_ARITHMETIC_GROUP, ['11{0}101', 0xae, 'd'], tstates=19,
       expand=['ii'])
    def XOR_A__ii_d_(self, ii, d):
        """ A <- A XOR ({0}+d) """
        assert_ii(ii)
        assert_d(d)
        self.XOR_A_n(self[RegisterPlusOffset(ii, d)])

    @I(EIGHT_BIT_ARITHMETIC_GROUP, [0xfe, 'n'], tstates=7)
    def CP_n(self, n, set_C_V=True):
        """ A - n """
        assert_n(n)
        a = self['A']
        n = (0x100 - n) % 0x100
        res = a + n
        res_modulo = res % 0x100
        HM = 0b00001111
        self['S'] = (res_modulo & 0b10000000)
        self['Z'] = (res_modulo == 0x00)
        self['5'] = (res_modulo & 0b00100000)
        self['H'] = ((a & HM) + (n & HM) > HM)
        self['3'] = (res_modulo & 0b00001000)
        self['N'] = True
        if set_C_V:
            MSB = 0b10000000
            overflow = (a & MSB) == (n & MSB) and\
                       (res_modulo & MSB) != (a & MSB)
            self['C'] = (res > 0x100)
            self['V'] = overflow

    @I(EIGHT_BIT_ARITHMETIC_GROUP, ['10111{0}'], tstates=4, expand=['r'])
    def CP_r(self, r):
        """ A - {0} """
        assert_r(r)
        self.CP_n(self[r])

    @I(EIGHT_BIT_ARITHMETIC_GROUP, [0xbe], tstates=7)
    def CP__HL_(self):
        """ A - (HL) """
        self.CP_n(self[self['HL']])

    @I(EIGHT_BIT_ARITHMETIC_GROUP, ['11{0}101', 0xbe, 'd'], tstates=19,
       expand=['ii'])
    def CP__ii_d_(self, ii, d):
        """ A - ({0}+d) """
        assert_ii(ii)
        assert_d(d)
        self.CP_n(self[RegisterPlusOffset(ii, d)])

    def INC_n(self, n):
        assert_n(n)
        HM = 0b00001111
        ret = (n + 1) % 0x100
        self['S'] = (ret & 0b10000000)
        self['Z'] = (ret == 0x00)
        self['5'] = (ret & 0b00100000)
        self['H'] = ((ret & HM) + (n & HM) > HM)
        self['3'] = (ret & 0b00001000)
        self['V'] = (n == 0x7e)
        self['N'] = False
        return ret

    @I(EIGHT_BIT_ARITHMETIC_GROUP, ['00{0}100'], tstates=4, expand=['r'])
    def INC_r(self, r):
        """ {0} <- {0} + 1 """
        assert_r(r)
        self[r] = self.INC_n(self[r])

    @I(EIGHT_BIT_ARITHMETIC_GROUP, [0x34], tstates=11)
    def INC__HL_(self):
        """ (HL) < (HL) + 1 """
        self[self['HL']] = self.INC_n(self['HL'])

    @I(EIGHT_BIT_ARITHMETIC_GROUP, ['11{0}101', 0x34, 'd'], tstates=23,
       expand=['ii'])
    def INC__ii_d_(self, ii, d):
        """ ({0} + d) <- ({0} + d) + 1 """
        assert_ii(ii)
        assert_d(d)
        tmp = self.INC_n(self[RegisterPlusOffset(ii, d)])
        self[RegisterPlusOffset(ii, d)] = tmp

    def DEC_n(self, n):
        assert_n(n)
        HM = 0b00001111
        ret = (n - 1) % 0x100
        self['S'] = (ret & 0b10000000)
        self['Z'] = (ret == 0x00)
        self['5'] = (ret & 0b00100000)
        self['H'] = ((ret & HM) + (n & HM) > HM)
        self['3'] = (ret & 0b00001000)
        self['V'] = (n == 0x80)
        self['N'] = True
        return ret

    @I(EIGHT_BIT_ARITHMETIC_GROUP, ['00{0}101'], tstates=4, expand=['r'])
    def DEC_r(self, r):
        """ {0} <- {0} - 1 """
        assert_r(r)
        self[r] = self.DEC_n(self[r])

    @I(EIGHT_BIT_ARITHMETIC_GROUP, [0x35], tstates=11)
    def DEC__HL_(self):
        """ (HL) < (HL) - 1 """
        self[self['HL']] = self.DEC_n(self['HL'])

    @I(EIGHT_BIT_ARITHMETIC_GROUP, ['11{0}101', 0x35, 'd'],
       tstates=23, expand=['ii'])
    def DEC__ii_d_(self, ii, d):
        """ ({0} + d) <- ({0} + d) - 1 """
        assert_ii(ii)
        assert_d(d)
        tmp = self.DEC_n(self[RegisterPlusOffset(ii, d)])
        self[RegisterPlusOffset(ii, d)] = tmp

    # ################
    # General purpose
    # ################
    @I(GENERAL_PURPOSE_GROUP, [0x00])
    def NOP(self):
        """ NOP """
        pass

    # ##################
    # 16 bit arithmetic
    # ##################
    def INC_PC(self, n=1):
        """ PC <- PC + n """
        assert_n(n)
        self['PC'] = (self['PC'] + n) % MEMSIZE

    def DEC_PC(self, n=1):
        """ PC <- PC - n """
        assert_n(n)
        self['PC'] = (self['PC'] - n) % MEMSIZE

    def ADD_mm_nn(self, mm, nn, carry=0):
        assert_nn(mm)
        assert_nn(nn)
        res = mm + nn + carry
        res_modulo = res % 0x10000
        HM = 0b0000111111111111
        self['H'] = ((mm & HM) + (nn & HM) + carry > HM)
        self['C'] = (res > 0x10000)
        return res_modulo

    def SUB_mm_nn(self, mm, nn, carry=0):
        assert_nn(nn)
        return self.ADD_mm_nn(mm, (MEMSIZE - nn) % MEMSIZE, carry)

    @I(SIXTEEN_BIT_ARITHMETIC_GROUP, ['00{0}1001'], tstates=11, expand=['ss'])
    def ADD_HL_ss(self, ss):
        """ HL <- HL + {0} """
        assert_ss(ss)
        self['HL'] = self.ADD_mm_nn(self['HL'], self[ss])

    @I(SIXTEEN_BIT_ARITHMETIC_GROUP, [0xed, '01{0}1010'], tstates=15,
       expand=['ss'])
    def ADC_HL_ss(self, ss):
        """ HL <- HL + {0} + CY """
        assert_ss(ss)
        self['HL'] = self.ADD_mm_nn(self['HL'], self[ss], carry=self['C'])

    @I(SIXTEEN_BIT_ARITHMETIC_GROUP, [0xed, '01{0}0010'], tstates=15,
       expand=['ss'])
    def SBC_HL_ss(self, ss):
        """ HL <- HL - {0} - CY """
        self['HL'] = self.SUB_mm_nn(self['HL'], self[ss], carry=self['C'])

    @I(SIXTEEN_BIT_ARITHMETIC_GROUP, [0xdd, '00{0}1001'], tstates=15,
       expand=['pp'])
    def ADD_IX_pp(self, pp):
        """ IX <- IX + {0} """
        assert_pp(pp)
        self['IX'] = self.ADD_mm_nn(self['IX'], self[pp])

    @I(SIXTEEN_BIT_ARITHMETIC_GROUP, [0xfd, '00{0}1001'], tstates=15,
       expand=['rr'])
    def ADD_IY_rr(self, rr):
        """ IY <- IY + {0} """
        assert_rr(rr)
        self['IY'] = self.ADD_mm_nn(self['IY'], self[rr])

    @I(SIXTEEN_BIT_ARITHMETIC_GROUP, ["00{0}0011"], tstates=6, expand=['ss'])
    def INC_ss(self, ss, n=1):
        """ {0} <- {0} + 1"""
        assert_ss(ss)
        self[ss] = (self[ss] + n) % MEMSIZE

    @I(SIXTEEN_BIT_ARITHMETIC_GROUP, ["11{0}101", 0x23],
       tstates=10, expand=['ii'])
    def INC_ii(self, ii, n=1):
        """ {0} <- {0} - 1 """
        assert_ii(ii)
        self[ii] = (self[ii] + n) % MEMSIZE

    @I(SIXTEEN_BIT_ARITHMETIC_GROUP, ["00{0}1011"], tstates=6, expand=['ss'])
    def DEC_ss(self, ss, n=1):
        """ {0} <- {0} - 1"""
        assert_ss(ss)
        self[ss] = (self[ss] - n) % MEMSIZE

    @I(SIXTEEN_BIT_ARITHMETIC_GROUP, ["11{0}101", 0x2b],
       tstates=10, expand=['ii'])
    def DEC_ii(self, ii, n=1):
        """ {0} <- {0} - 1"""
        assert_ii(ii)
        self[ii] = (self[ii] - n) % MEMSIZE

    # ################
    # rotate and shift
    # ################
    def _set_flags_after_shift_(self, n, carry=None):
        MSB = 0b10000000
        self['S'] = (n & MSB)
        self['Z'] = (n == 0x00)
        self['5'] = False
        self['H'] = False
        self['3'] = False
        self['P'] = parity(n)
        self['N'] = False
        if carry is not None:
            self['C'] = carry

    def RLC_n(self, n):
        """ Bits of n are shifted left by one position.
            Bit 7 is copied to flag C and to position 0.
            Returns new value.
        """
        assert_n(n)
        MSB = 0b10000000
        carry = 1 if (MSB & n) else 0
        n = (n << 1) | carry
        self._set_flags_after_shift_(n, carry)
        return n

    def RL_n(self, n):
        """ Bits of n are shifted left by one position.
            Bit 7 is copied to flag C. The old value of C is copied to bit 0.
            Returns new value.
        """
        assert_n(n)
        MSB = 0b10000000
        carry = 1 if (MSB & n) else 0
        n = (n << 1) | self['C']
        self._set_flags_after_shift_(n, carry)
        return n

    def SLA_n(self, n):
        """ Bits of n are shifted left by one position.
            Bit 7 is copied to flag C. Bit 0 is unset.
            Returns new value.
        """
        assert_n(n)
        MSB = 0b10000000
        carry = 1 if (MSB & n) else 0
        n = (n << 1)
        self._set_flags_after_shift_(n, carry)
        return n

    def RRC_n(self, n):
        """ Bits of n are shifted right by one position.
            Bit 0 is copied to flag C and to bit 7
            Returns new value.
        """
        assert_n(n)
        LSB = 0b00000001
        MSB = 0b10000000
        carry = MSB if (LSB & n) else 0
        n = (n >> 1) | carry
        self._set_flags_after_shift_(n, carry)
        return n

    def RR_n(self, n):
        """ Bits of n are shifted right by one position.
            Bit 0 is copied to flag C. Carry bit is copied to bit 7.
            Returns new value.
        """
        assert_n(n)
        LSB = 0b00000001
        MSB = 0b10000000
        carry = MSB if (LSB & n) else 0
        n = (n >> 1) | (self['C'] << 7)
        self._set_flags_after_shift_(n, carry)
        return n

    def SRL_n(self, n):
        """ Bits of n are shifted right by one position.
            Bit 0 is copied to flag C. Bit 7 is unset.
            Returns new value.
        """
        assert_n(n)
        LSB = 0b00000001
        MSB = 0b10000000
        carry = MSB if (LSB & n) else 0
        n = (n >> 1)
        self._set_flags_after_shift_(n, carry)
        return n

    def SRA_n(self, n):
        """ Bits of n are shifted right by one position.
            Bit 0 is copied to flag C. Bit 7 is not changed.
            Returns new value.
        """
        assert_n(n)
        LSB = 0b00000001
        MSB = 0b10000000
        carry = MSB if (LSB & n) else 0
        n = (n >> 1) | (n & MSB)
        self._set_flags_after_shift_(n, carry)
        return n

    def RLD_n(self, n):
        """ The contents of bits 3,2,1,0 of n are copied to
            the bits 7,6,5,4 of n.
            The previous content of bits 7,6,5,4 are copied to
            the bits 3,2,1,0 of A.
            The previous contents of the bits 3,2,1,0 of A are copied
            to the bits 3,2,1,0 of n.
            Returns new value of n.
        """
        #         +----------+
        # A       |  n      \|/
        # 7..4 3..0  7..4 3..0
        #     /|\    | /|\   |
        #      +-----+  +----+
        assert_n(n)
        a = self['A']
        LSB = 0b00001111
        MSB = 0b11110000
        la = a & LSB
        a = (a & MSB) | ((n & MSB) >> 4)
        n = (n << 4) | la
        self['A'] = a
        self._set_flags_after_shift_(a)
        return n

    def RRD_n(self, n):
        """ The contents of bits 7,8,5,4 of n are copied to
            the bits 3,2,1,0 of n.
            The previous content of bits 3,2,1,0 are copied to
            the bits 3,2,1,0 of A.
            The previous contents of the bits 3,2,1,0 of A are copied
            to the bits 7,2,1,0 of n.
            Returns new value of n.
        """
        #         +----------+
        # A      \|/ n       |
        # 7..4 3..0  7..4 3..0
        #      |    /|\ |   /|\
        #      +-----+  +----+
        assert_n(n)
        a = self['A']
        LSB = 0b00001111
        MSB = 0b11110000
        la = a & LSB
        a = (a & MSB) | (n & LSB)
        n = (n >> 4) | (la << 4)
        self['A'] = a
        self._set_flags_after_shift_(a)
        return n

    @I(ROTATE_AND_SHIFT_GROUP, [0x07], tstates=4)
    def RLCA(self):
        """ A0 << A7
            CY << A """
        self['A'] = self.RLC_n(self['A'])

    @I(ROTATE_AND_SHIFT_GROUP, [0x17], tstates=4)
    def RLA(self):
        """ A0 << CY
            CY << A """
        self['A'] = self.RLA_n(self['A'])

    @I(ROTATE_AND_SHIFT_GROUP, [0x0f], tstates=4)
    def RRCA(self):
        """ A0 >> A7
            A >> CY """
        self['A'] = self.RRC_n(self['A'])

    @I(ROTATE_AND_SHIFT_GROUP, [0x1f], tstates=4)
    def RRA(self):
        """ CY >> A7
            A >> CY """
        self['A'] = self.RR_n(self['A'])

    @I(ROTATE_AND_SHIFT_GROUP, [0xcb, '00000{0}'], tstates=8, expand=['r'])
    def RLC_r(self, r):
        """ {0}0 << {0}7
            CY << {0} """
        assert_r(r)
        self[r] = self.RLC_n(self[r])

    @I(ROTATE_AND_SHIFT_GROUP, [0xcb, 0x06], tstates=15)
    def RLC__HL_(self):
        """ (HL)0 << (HL)7
            CY << (HL) """
        self[self['HL']] = self.RLC_n(self[self['HL']])

    @I(ROTATE_AND_SHIFT_GROUP, ['11{0}101', 0xcb, 'd', 0x06], tstates=23,
       expand=['ii'])
    def RLC__ii_d_(self, ii, d):
        """ ({0}+d)0 << ({0}+d)7
            CY << ({0}+d) """
        assert_ii(ii)
        assert_d(d)
        nn = RegisterPlusOffset(ii, d)
        self[nn] = self.RLC_n(self[nn])

    @I(ROTATE_AND_SHIFT_GROUP, [0xcb, '00010{0}'], tstates=8, expand=['r'])
    def RL_r(self, r):
        """ {0}0 << CY
            CY << {0} """
        assert_r(r)
        self[r] = self.RL_n(self[r])

    @I(ROTATE_AND_SHIFT_GROUP, [0xcb, 0x16], tstates=15)
    def RL__HL_(self):
        """ (HL)0 << CY
            CY << (HL) """
        self[self['HL']] = self.RL_n(self[self['HL']])

    @I(ROTATE_AND_SHIFT_GROUP, ['11{0}101', 0xcb, 'd', 0x16], tstates=23,
       expand=['ii'])
    def RL__ii_d_(self, ii, d):
        """ ({0}+d)0 << CY
             CY << ({0}+d) """
        assert_ii(ii)
        assert_d(d)
        nn = RegisterPlusOffset(ii, d)
        self[nn] = self.RL_n(self[nn])

    @I(ROTATE_AND_SHIFT_GROUP, [0xcb, '00001{0}'], tstates=8, expand=['r'])
    def RRC_r(self, r):
        """ {0}0 >> {0}7
            {0} >> CY """
        assert_r(r)
        self[r] = self.RRC_n(self[r])

    @I(ROTATE_AND_SHIFT_GROUP, [0xcb, 0x0e], tstates=15)
    def RRC__HL_(self):
        """ (HL)0 >> (HL)7
        (HL) >> CY """
        self[self['HL']] = self.RRC_n(self[self['HL']])

    @I(ROTATE_AND_SHIFT_GROUP, ['11{0}101', 0xcb, 'd', 0x0e], tstates=23,
       expand=['ii'])
    def RRC__ii_d_(self, ii, d):
        """ ({0}+d)0 >> ({0}+d)7, ({0}+d) >> CY """
        assert_ii(ii)
        assert_d(d)
        nn = RegisterPlusOffset(ii, d)
        self[nn] = self.RRC_n(self[nn])

    @I(ROTATE_AND_SHIFT_GROUP, [0xcb, '00011{0}'], tstates=8, expand=['r'])
    def RR_r(self, r):
        """ {0}0 >> CY, {0} >> CY """
        assert_r(r)
        self[r] = self.RR_n(self[r])

    @I(ROTATE_AND_SHIFT_GROUP, [0xcb, 0x1e], tstates=15)
    def RR__HL_(self):
        """ (HL)0 >> CY
        (HL) >> CY """
        self[self['HL']] = self.RR_n(self[self['HL']])

    @I(ROTATE_AND_SHIFT_GROUP, ['11{0}101', 0xcb, 'd', 0x1e], tstates=23,
       expand=['ii'])
    def RR__ii_d_(self, ii, d):
        """ ({0}+d)0 >> CY, CY >> ({0}+d) """
        assert_ii(ii)
        assert_d(d)
        nn = RegisterPlusOffset(ii, d)
        self[nn] = self.RR_n(self[nn])

    @I(ROTATE_AND_SHIFT_GROUP, [0xcb, '00100{0}'], tstates=8, expand=['r'])
    def SLA_r(self, r):
        """ CY << {0}7
            {0} << 0 """
        assert_r(r)
        self[r] = self.SLA_n(self[r])

    @I(ROTATE_AND_SHIFT_GROUP, [0xcb, 0x26], tstates=15)
    def SLA__HL_(self):
        """ CY << (HL)7
            (HL) << 0 """
        self[self['HL']] = self.SLA_n(self[self['HL']])

    @I(ROTATE_AND_SHIFT_GROUP, ['11{0}101', 0xcb, 'd', 0x26], tstates=23,
       expand=['ii'])
    def SLA__ii_d_(self, ii, d):
        """ CY << ({0}+d)7
            ({0}+d) << 0 """
        assert_ii(ii)
        assert_d(d)
        nn = RegisterPlusOffset(ii, d)
        self[nn] = self.SLA_n(self[nn])

    @I(ROTATE_AND_SHIFT_GROUP, [0xcb, '00101{0}'], tstates=8, expand=['r'])
    def SRA_r(self, r):
        """ {0}7 >> {0}7
            {0} >> CY """
        assert_r(r)
        self[r] = self.SRA_n(self[r])

    @I(ROTATE_AND_SHIFT_GROUP, [0xcb, 0x2e], tstates=15)
    def SRA__HL_(self):
        """ (HL)7 >> (HL)7
            (HL) >> CY """
        self[self['HL']] = self.SRA_n(self[self['HL']])

    @I(ROTATE_AND_SHIFT_GROUP, ['11{0}101', 0xcb, 'd', 0x2e], tstates=23,
       expand=['ii'])
    def SRA__ii_d_(self, ii, d):
        """ ({0}+d)7 >> ({0}+d)7
        ({0}+d) >> CY """
        assert_ii(ii)
        assert_d(d)
        nn = RegisterPlusOffset(ii, d)
        self[nn] = self.SRA_n(self[nn])

    @I(ROTATE_AND_SHIFT_GROUP, [0xcb, '00111{0}'], tstates=8, expand=['r'])
    def SRL_r(self, r):
        """ 0 >> {0}7, {0} >> CY """
        assert_r(r)
        self[r] = self.SRL_n(self[r])

    @I(ROTATE_AND_SHIFT_GROUP, [0xcb, 0x3e], tstates=15)
    def SRL__HL_(self):
        """ 0 >> (HL)7
            (HL) >> CY """
        self[self['HL']] = self.SRL_n(self[self['HL']])

    @I(ROTATE_AND_SHIFT_GROUP, ['11{0}101', 0xcb, 'd', 0x3e], tstates=23,
       expand=['ii'])
    def SRL__ii_d_(self, ii, d):
        """ 0 >> ({0}+d)7, ({0}+d) >> CY """
        assert_ii(ii)
        assert_d(d)
        nn = RegisterPlusOffset(ii, d)
        self[nn] = self.SRL_n(self[nn])

    @I(ROTATE_AND_SHIFT_GROUP, [0xed, 0x6f], tstates=18)
    def RLD(self):
        """ RLD """
        self[self['HL']] = self.RLD_n(self[self['HL']])

    @I(ROTATE_AND_SHIFT_GROUP, [0xed, 0x67], tstates=18)
    def RRD(self):
        """ RRD """
        self[self['HL']] = self.RRD_n(self[self['HL']])

    # #######################
    # Bit set, reset and test
    # #######################
    def BIT_b_n(self, b, n):
        assert_b(b)
        assert_n(n)
        self['H'] = True
        self['N'] = False
        self['Z'] = False if (1 << b) & n else True

    def SET_b_n(self, b, n, state=1):
        assert_b(b)
        assert_n(n)
        if state:
            return n | (1 << b)
        else:
            return n & (0xff ^ (1 << b))

    @I(BIT_SET_RESET_TEST_GROUP, [0xcb, '01{0}{1}'], tstates=8,
       expand=['b', 'r'])
    def BIT_b_r(self, b, r):
        """ Z <- not({1}{0}) """
        assert_b(b)
        assert_r(r)
        self.BIT_b_n(b, self[r])

    @I(BIT_SET_RESET_TEST_GROUP, [0xcb, '01{0}110'], tstates=12,
       expand=['b'])
    def BIT_b__HL_(self, b):
        """ Z <- not((HL){0}) """
        assert_b(b)
        self.BIT_b_n(b, self[self['HL']])

    @I(BIT_SET_RESET_TEST_GROUP, ['11{1}101', 0xcb, 'd', '01{0}110'],
       tstates=20, expand=['b', 'ii'])
    def BIT_b__ii_d_(self, b, ii, d):
        """ Z <- not(({1} +d)) """
        assert_ii(ii)
        assert_d(d)
        nn = RegisterPlusOffset(ii, d)
        self.BIT_b_n(b, self[nn])

    @I(BIT_SET_RESET_TEST_GROUP, [0xcb, '11{0}{1}'], tstates=8,
       expand=['b', 'r'])
    def SET_b_r(self, b, r):
        """ {1}{0} <- 1 """
        assert_b(b)
        assert_r(r)
        self[r] = self.SET_b_n(b, self[r])

    @I(BIT_SET_RESET_TEST_GROUP, [0xcb, '11{0}110'], tstates=15, expand=['b'])
    def SET_b__HL_(self, b):
        """ (HL){0} <- 1 """
        assert_b(b)
        self[self['HL']] = self.SET_b_n(b, self[self['HL']])

    @I(BIT_SET_RESET_TEST_GROUP, ['11{1}101', 0xcb, 'd', '11{0}110'],
       tstates=23, expand=['b', 'ii'])
    def SET_b__ii_d_(self, b, ii, d):
        """ ({1}+d){0} <- 0 """
        assert_b(b)
        assert_ii(ii)
        assert_d(d)
        nn = RegisterPlusOffset(ii, d)
        self[nn] = self.SET_b_n(b, self[nn])

    @I(BIT_SET_RESET_TEST_GROUP, [0xcb, '10{0}{1}'], tstates=8,
       expand=['b', 'r'])
    def RES_b_r(self, b, r):
        """ {1}{0} <- 0 """
        assert_b(b)
        assert_r(r)
        self[r] = self.SET_b_n(b, self[r], state=False)

    @I(BIT_SET_RESET_TEST_GROUP, [0xcb, '10{0}110'], tstates=15, expand=['b'])
    def RES_b__HL_(self, b):
        """ (HL){0} <- 0 """
        assert_b(b)
        self[self['HL']] = self.SET_b_n(b, self[self['HL']], state=False)

    @I(BIT_SET_RESET_TEST_GROUP, ['11{1}101', 0xcb, 'd', '10{0}110'],
       tstates=23, expand=['b', 'ii'])
    def RES_b__ii_d_(self, b, ii, d):
        """ ({1}+d){0} <- 0 """
        assert_b(b)
        assert_ii(ii)
        assert_d(d)
        nn = RegisterPlusOffset(ii, d)
        self[nn] = self.SET_b_n(b, self[nn], state=False)

    # #######################
    # jump
    # #######################

    # #######################
    # call and return
    # #######################

    # #######################
    # input and output
    # #######################
