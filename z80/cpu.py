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
from assertions import assert_q
from assertions import assert_r
from assertions import assert_b
from assertions import assert_ii
from assertions import assert_aa
from assertions import assert_ss
from assertions import assert_flag

from util import parity
from util import n2d
from instruction_group import InstructionGroup
from instruction_group import InstructionDecor as I
from register import RegisterSet
from register import RegisterPlusOffset
from register import PC
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
GENERAL_PURPOSE = InstructionGroup("general purpose group",
                                   ALL_INSTRUCTIONS)
SIXTEEN_BIT_ARITHMETIC_GROUP = InstructionGroup("16 bit arithmetic group",
                                                ALL_INSTRUCTIONS)
ROTATE_AND_SHIFT_GROUP = InstructionGroup("rotate and shift group",
                                          ALL_INSTRUCTIONS)


# todo remove this
import instr_templates as it
from instr_template_expansion import expand_template
from instruction import Instruction


def add_instruction_group(group, instr_set):
    grp = group.name
    for entry in instr_set:
        for expanded in expand_template(entry):
            instr = Instruction(assembler=expanded['instr'],
                                opcode=list(expanded['opcode']),
                                func=expanded['func'],
                                tstates=expanded['tstates'],
                                operation=expanded['operation'],
                                group=grp)
            group.add(instr)


add_instruction_group(EIGHT_BIT_LOAD_GROUP,
                      it.EIGHT_BIT_LOAD_GROUP)
add_instruction_group(SIXTEEN_BIT_LOAD_GROUP,
                      it.SIXTEEN_BIT_LOAD_GROUP)
add_instruction_group(EXCHANGE_GROUP,
                      it.EXCHANGE_GROUP)
add_instruction_group(BLOCK_TRANSFER_GROUP,
                      it.BLOCK_TRANSFER_GROUP)
add_instruction_group(SEARCH_GROUP,
                      it.SEARCH_GROUP)
add_instruction_group(EIGHT_BIT_ARITHMETIC_GROUP,
                      it.EIGHT_BIT_ARITHMETIC_GROUP)
add_instruction_group(GENERAL_PURPOSE,
                      it.GENERAL_PURPOSE)
add_instruction_group(SIXTEEN_BIT_ARITHMETIC_GROUP,
                      it.SIXTEEN_BIT_ARITHMETIC_GROUP)
add_instruction_group(ROTATE_AND_SHIFT_GROUP,
                      it.ROTATE_AND_SHIFT_GROUP)

# end remove


class CPU(object):
    def __init__(self):
        self.reg = RegisterSet()

    def __getitem__(self, key):
        return self.reg[key]

    def __setitem__(self, key, value):
        self.reg[key] = value

    def fetch(self):
        # todo 4 byte instructions
        code1 = self['PC']
        if code1 in ALL_INSTRUCTIONS:
            if isinstance(ALL_INSTRUCTIONS[code1], dict):
                code2 = self[PC(1)]
                if code2 in ALL_INSTRUCTIONS[code1]:
                    return ALL_INSTRUCTIONS[code1][code2]
                else:
                    return None
            else:
                return ALL_INSTRUCTIONS[code1]
        else:
            raise NotImplemented('instruction not implemented %02x' % code1)

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

    @I(EIGHT_BIT_LOAD_GROUP, [0x36, "n"])
    def LD__HL__n(self, n):
        """ (HL) <- n """
        assert_r(n)
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

    # ########################################
    def LD_A_n(self, n):
        """ LD A,n """
        assert_n(n)
        self.reg['A'] = n

    def LD_F_n(self, n):
        """ LD F, n"""
        assert_n(n)
        self.reg['F'] = n

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

    def LD_ref_HL_n(self, n):
        """ LD (HL), n"""
        self.LD_ref_nn_n(self.GET_HL(), n)

    def LD_ref_index_plus_d(self, idx, n, pc_offset=2):
        """LD (idx + (PC+pc_offset)), n"""
        self.LD_ref_nn_n(self.GET_index_plus_d(idx, pc_offset), n)

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

    def LD_ii_nn(self, ii, nn):
        """ LD dd, nn"""
        assert_ii(ii)
        assert_nn(nn)
        if ii == 'SP':
            self.LD_SP_nn(nn)
        elif ii == 'PC':
            self.LD_PC_nn(nn)
        elif ii == 'IX':
            self.LD_IX_nn(nn)
        elif ii == 'IY':
            self.LD_IY_nn(nn)
        elif ii == 'AF':
            self.LD_F_n(nn & 0x00ff)
            self.LD_A_n(nn >> 8)
        else:
            self.LD_r_n(ii[1], nn & 0x00ff)
            self.LD_r_n(ii[0], nn >> 8)

    def LD_index_nn(self, index, nn):
        """ LD IX, nn or LD IY, nn"""
        assert_ii(index)
        assert_nn(nn)
        setattr(self, index, nn)

    def LD_ref2_nn_nn(self, nn1, nn2):
        """ LD (nn), nn"""
        assert_nn(nn1)
        assert_n(nn2)
        self.LD_ref_nn_n(nn1, nn2 & 0xff)
        self.LD_ref_nn_n((nn1 + 1) % CPU.MEMSIZE, nn2 >> 8)

    def PUSH_qq(self, qq):
        self.DEC_SP(2)
        self.LD_ref_nn_nn(self.GET_SP(), self.GET_ii(qq))

    def PUSH_ii(self, ii):
        self.DEC_SP(2)
        self.LD_ref_nn_nn(self.GET_SP(), self.GET_ii(ii))

    def POP_qq(self, qq):
        self.LD_ii_nn(qq, self.GET_ref_nn(self.GET_SP()))
        self.INC_SP(2)

    def POP_ii(self, ii):
        self.LD_ii_nn(ii, self.GET_ref_nn(self.GET_SP()))
        self.INC_SP(2)

    # 8 bit getter #
    def GET_r(self, r):
        """B,C,D,E,H,L or A"""
        # todo replace by GET_s
        assert_r(r)
        return self.reg[r]

    def GET_A(self):
        return self.reg['A']

    def GET_F(self):
        return self.reg['F']

    def GET_I(self):
        return self.reg['I']

    def GET_R(self):
        return self.reg['R']

    def GET_ref_nn(self, nn):
        """(nn)"""
        assert_nn(nn)
        return self.mem[nn]

    def GET_ref_PC_plus_d(self, d):
        """
        returns (PC+d)
        eq. to self.GET_ref_nn(self.GET_ii_plus_d('PC', 1)))
        """
        return self.mem[self.GET_ii_plus_d('PC', d)]

    def GET_ref_HL(self):
        """(HL)"""
        return self.GET_ref_nn(self.GET_HL())

    def GET_ref_index_plus_d(self, idx, pc_offset=2):
        """(idx + (PC+pc_offset))"""
        return self.GET_ref_nn(self.GET_index_plus_d(idx, pc_offset))

    # 16 bit getter #
    def GET_PC(self):
        return self.PC

    def GET_SP(self):
        return self.SP

    def GET_BC(self):
        return self.reg['BC']

    def GET_DE(self):
        return self.reg['DE']

    def GET_HL(self):
        return self.reg['HL']

    def GET_AF(self):
        return self.reg['AF']

    def GET_IX(self):
        return self.IX

    def GET_IY(self):
        return self.IY

    def GET_IR(self):
        return (self.I << 8) + self.R

    def GET_ss(self, ss):
        assert_ss(ss)
        getter = getattr(self, 'GET_' + ss)
        return getter()

    def GET_ii(self, ii):
        assert_aa(ii)
        getter = getattr(self, 'GET_' + ii)
        return getter()

    def GET_ii_plus_d(self, ii, d):
        """ ii + d """
        assert_d(d)
        nn = self.GET_ii(ii)
        return (nn + d) % CPU.MEMSIZE

    def GET_index_plus_d(self, idx, pc_offset=2):
        """idx + (PC+pc_offset)"""
        d = n2d(self.GET_ref_PC_plus_d(pc_offset))
        return self.GET_ii_plus_d(idx, d)

    def GET_ref2_nn(self, nn):
        """(nn+1) << 8 + (nn)"""
        assert_nn(nn)
        msb = self.mem[(nn + 1) % CPU.MEMSIZE] << 8
        return msb + self.mem[nn]

    def GET_ref2_PC_plus_d(self, d):
        """ eq. to self.GET_ref2_nn(self.GET_ii_plus_d('PC', 1)))"""
        return self.GET_ref2_nn(self.GET_ii_plus_d('PC', d))

    # exchange
    def EX_q_altq(self, q):
        assert_q(q)
        alt_value = getattr(self.alt_register_set, q)
        main_value = getattr(self.main_register_set, q)
        setattr(self.main_register_set, q, alt_value)
        setattr(self.alt_register_set, q, main_value)

    def EX_DE_HL(self):
        tmp = self.GET_DE()
        self.LD_ii_nn('DE', self.GET_HL())
        self.LD_ii_nn('HL', tmp)

    def EX_AF_altAF(self):
        self.EX_q_altq('A')
        self.EX_q_altq('F')

    def EXX(self):
        self.EX_q_altq('B')
        self.EX_q_altq('C')
        self.EX_q_altq('D')
        self.EX_q_altq('E')
        self.EX_q_altq('H')
        self.EX_q_altq('L')

    def EX_ref_SP_HL(self):
        tmp = self.GET_ref2_nn(self.SP())
        self.LD_ref2_nn_nn(self.SP(), self.GET_HL())
        self.LD_ii('HL', tmp)

    def EX_ref_SP_ii(self, ii):
        tmp = self.GET_ref2_nn(self.SP())
        self.LD_ref2_nn_nn(self.SP(), self.GET_ii(ii))
        self.LD_ii(ii, tmp)

    # block transfer group
    def LDI(self):
        self.LD_ref_nn_n(self.GET_DE(), self.GET_ref_nn(self.GET_HL()))
        self.INC_ii('DE')
        self.INC_ii('HL')
        self.DEC_ii('BC')
        self.UNSET_FLAG('H')
        self.UNSET_FLAG('N')
        if self.GET_BC() == 1:
            self.SET_FLAG('V')
        else:
            self.UNSET_FLAG('V')

    def LDIR(self):
        self.LDI()
        if self.GET_BC() != 0x0000:
            self.DEC_PC(2)

    def LDD(self):
        self.LD_ref_nn_n(self.GET_DE(), self.GET_ref_nn(self.GET_HL()))
        self.DEC_ii('DE')
        self.DEC_ii('HL')
        self.DEC_ii('BC')
        self.UNSET_FLAG('H')
        self.UNSET_FLAG('N')
        if self.GET_BC() == 1:
            self.SET_FLAG('V')
        else:
            self.UNSET_FLAG('V')

    def LDDR(self):
        self.LDD()
        if self.GET_BC() != 0x0000:
            self.DEC_PC(2)

    # search
    def CPI(self):
        self.CP_A_n(self.GET_ref_nn(self.GET_HL()), False)
        self.SET_FLAG('V', self.GET_BC() != 0x00001)
        self.INC_ii('HL')
        self.DEC_ii('BC')

    def CPIR(self):
        self.CPI()
        if self.GET_BC() != 0x0000:
            self.DEC_PC(2)

    def CPD(self):
        self.CP_A_n(self.GET_ref_nn(self.GET_HL()), False)
        self.SET_FLAG('V', self.GET_BC() != 0x00001)
        self.DEC_ii('HL')
        self.DEC_ii('BC')

    def CPDR(self):
        self.CPD()
        if self.GET_BC() != 0x0000:
            self.DEC_PC(2)

    # bitwise / flags set / get
    def SET_FLAG(self, flag, state=1):
        assert_flag(flag)
        if state:
            self.reg[flag] = 1
        else:
            self.reg[flag] = 0

    def SET_b_n(self, b, n, state=1):
        assert_b(b)
        assert_n(n)
        if state:
            return n | (1 << b)
        else:
            return n & (0xff ^ (1 << b))

    def SET_b_r(self, b, r, state=1):
        assert_r(r)
        self.LD_r_n(r, self.SET_b_n(b, self.GET_r(r), state))

    def SET_b_ref_nn(self, b, nn, state=1):
        assert_nn(nn)
        self.LD_ref_nn_n(nn, self.SET_b_n(b, self.GET_ref_nn(nn), state))

    def GET_FLAG(self, flag):
        assert_flag(flag)
        return self.reg[flag]

    def GET_FLAGS(self, V_or_P='V'):
        if V_or_P == 'V':
            flags = 'SZ5H3VNC'
        else:
            flags = 'SZ5H3PNC'
        ret = ''
        for f in flags:
            if self.GET_FLAG(f):
                ret += f
        return ret

    def BIT_b_n(self, b, n):
        assert_b(b)
        assert_n(n)
        self.SET_FLAG('H')
        self.SET_FLAG('N', 0)
        if (1 << b) & n:
            self.SET_FLAG('Z', 0)
        else:
            self.SET_FLAG('Z', 1)

    # rotate and shift group
    def RLC_r(self, r):
        self.LD_r_n(r, self.shift_left_n(self.reg[r], 'RLC'))

    def RLC_ref_HL(self):
        nn = self.GET_HL()
        self.LD_ref_nn_n(nn, self.shift_left_n(self.GET_ref_nn(nn), 'RLC'))

    def RLC_ref_index_plus_d(self, ii):
        d = n2d(self.GET_ref_PC_plus_d(2))
        nn = self.GET_ii_plus_d(ii, d)
        self.LD_ref_nn_n(nn, self.shift_left_n(self.GET_ref_nn(nn), 'RLC'))

    # RL #
    def RL_r(self, r):
        self.LD_r_n(r, self.shift_left_n(self.GET_r(r), 'RL'))

    def RL_ref_HL(self):
        nn = self.GET_HL()
        self.LD_ref_nn_n(nn, self.shift_left_n(self.GET_ref_nn(nn), 'RL'))

    def RL_ref_index_plus_d(self, ii):
        d = n2d(self.GET_ref_PC_plus_d(2))
        nn = self.GET_ii_plus_d(ii, d)
        self.LD_ref_nn_n(nn, self.shift_left_n(self.GET_ref_nn(nn), 'RL'))

    # SLA #
    def SLA_r(self, r):
        self.LD_r_n(r, self.shift_left_n(self.GET_r(r), 'SLA'))

    def SLA_ref_HL(self):
        nn = self.GET_HL()
        self.LD_ref_nn_n(nn, self.shift_left_n(self.GET_ref_nn(nn), 'SLA'))

    def SLA_ref_index_plus_d(self, ii):
        d = n2d(self.GET_ref_PC_plus_d(2))
        nn = self.GET_ii_plus_d(ii, d)
        self.LD_ref_nn_n(nn, self.shift_left_n(self.GET_ref_nn(nn), 'SLA'))

    # RRC #
    def RRC_r(self, r):
        self.LD_r_n(r, self.shift_right_n(self.GET_r(r), 'RRC'))

    def RRC_ref_HL(self):
        nn = self.GET_HL()
        self.LD_ref_nn_n(nn, self.shift_right_n(self.GET_ref_nn(nn), 'RRC'))

    def RRC_ref_index_plus_d(self, ii):
        d = n2d(self.GET_ref_PC_plus_d(2))
        nn = self.GET_ii_plus_d(ii, d)
        self.LD_ref_nn_n(nn, self.shift_right_n(self.GET_ref_nn(nn), 'RRC'))

    # RR #
    def RR_r(self, r):
        self.LD_r_n(r, self.shift_right_n(self.GET_r(r), 'RR'))

    def RR_ref_HL(self):
        nn = self.GET_HL()
        self.LD_ref_nn_n(nn, self.shift_right_n(self.GET_ref_nn(nn), 'RR'))

    def RR_ref_index_plus_d(self, ii):
        d = n2d(self.GET_ref_PC_plus_d(2))
        nn = self.GET_ii_plus_d(ii, d)
        self.LD_ref_nn_n(nn, self.shift_right_n(self.GET_ref_nn(nn), 'RR'))

    # SRA #
    def SRA_r(self, r):
        self.LD_r_n(r, self.shift_right_n(self.GET_r(r), 'SRA'))

    def SRA_ref_HL(self):
        nn = self.GET_HL()
        self.LD_ref_nn_n(nn, self.shift_right_n(self.GET_ref_nn(nn), 'SRA'))

    def SRA_ref_index_plus_d(self, ii):
        d = n2d(self.GET_ref_PC_plus_d(2))
        nn = self.GET_ii_plus_d(ii, d)
        self.LD_ref_nn_n(nn, self.shift_right_n(self.GET_ref_nn(nn), 'SRA'))

    # SRL #
    def SRL_r(self, r):
        self.LD_r_n(r, self.shift_right_n(self.GET_r(r), 'SRL'))

    def SRL_ref_HL(self):
        nn = self.GET_HL()
        self.LD_ref_nn_n(nn, self.shift_right_n(self.GET_ref_nn(nn), 'SRL'))

    def SRL_ref_index_plus_d(self, ii):
        d = n2d(self.GET_ref_PC_plus_d(2))
        nn = self.GET_ii_plus_d(ii, d)
        self.LD_ref_nn_n(nn, self.shift_right_n(self.GET_ref_nn(nn), 'SRL'))

    # RLD RRD #
    def RLD(self):
        nn = self.GET_HL()
        self.LD_ref_nn_n(nn, self.RLD_n(self.GET_ref_nn(nn)))

    def RRD(self):
        nn = self.GET_HL()
        self.LD_ref_nn_n(nn, self.RRD_n(self.GET_ref_nn(nn)))

    # 8 bit arithmetic
    def ADD_A_n(self, n, carry=0):
        assert_n(n)
        a = self.GET_A()
        res = a + n + carry
        res_modulo = res % 0x100
        HM = 0b00001111
        MSB = 0b10000000
        overflow = (a & MSB) == (n & MSB) and (res_modulo & MSB) != (a & MSB)
        self.SET_FLAG('S', res_modulo & 0b10000000)
        self.SET_FLAG('Z', res_modulo == 0x00)
        self.SET_FLAG('5', res_modulo & 0b00100000)
        # todo check H flag
        self.SET_FLAG('H', (a & HM) + (n & HM) + carry > HM)
        self.SET_FLAG('3', res_modulo & 0b00001000)
        self.SET_FLAG('V', overflow)
        self.SET_FLAG('N', False)
        self.SET_FLAG('C', res > 0x100)
        self.LD_A_n(res_modulo)

    def SUB_A_n(self, n, carry=0):
        assert_n(n)
        self.ADD_A_n((0x100 - n) % 0x100, carry)

    def AND_A_n(self, n):
        assert_n(n)
        a = self.GET_A()
        a &= n
        self.SET_FLAG('S', a & 0b10000000)
        self.SET_FLAG('Z', a == 0x00)
        self.SET_FLAG('H', True)
        self.SET_FLAG('P', parity(a))
        self.SET_FLAG('N', False)
        self.SET_FLAG('C', False)
        self.LD_A_n(a)

    def OR_A_n(self, n):
        assert_n(n)
        a = self.GET_A()
        a |= n
        self.SET_FLAG('S', a & 0b10000000)
        self.SET_FLAG('Z', a == 0x00)
        self.SET_FLAG('H', True)
        self.SET_FLAG('P', parity(a))
        self.SET_FLAG('N', False)
        self.SET_FLAG('C', False)
        self.LD_A_n(a)

    def XOR_A_n(self, n):
        assert_n(n)
        a = self.GET_A()
        a ^= n
        self.SET_FLAG('S', a & 0b10000000)
        self.SET_FLAG('Z', a == 0x00)
        self.SET_FLAG('H', True)
        self.SET_FLAG('P', parity(a))
        self.SET_FLAG('N', False)
        self.SET_FLAG('C', False)
        self.LD_A_n(a)

    def CP_A_n(self, n, set_C_V=True):
        assert_n(n)
        a = self.GET_A()
        n = (0x100 - n) % 0x100
        res = a + n
        res_modulo = res % 0x100
        HM = 0b00001111
        self.SET_FLAG('S', res_modulo & 0b10000000)
        self.SET_FLAG('Z', res_modulo == 0x00)
        self.SET_FLAG('5', res_modulo & 0b00100000)
        self.SET_FLAG('H', (a & HM) + (n & HM) > HM)
        self.SET_FLAG('3', res_modulo & 0b00001000)
        self.SET_FLAG('N', True)
        if set_C_V:
            MSB = 0b10000000
            overflow = (a & MSB) == (n & MSB) and\
                       (res_modulo & MSB) != (a & MSB)
            self.SET_FLAG('C', res > 0x100)
            self.SET_FLAG('V', overflow)

    def INC_n(self, n):
        assert_n(n)
        HM = 0b00001111
        ret = (n + 1) % 0x100
        self.SET_FLAG('S', ret & 0b10000000)
        self.SET_FLAG('Z', ret == 0x00)
        self.SET_FLAG('5', ret & 0b00100000)
        self.SET_FLAG('H', (ret & HM) + (n & HM) > HM)
        self.SET_FLAG('3', ret & 0b00001000)
        self.SET_FLAG('V', n == 0x7e)
        self.SET_FLAG('N', False)
        return ret

    def DEC_n(self, n):
        assert_n(n)
        HM = 0b00001111
        ret = (n - 1) % 0x100
        self.SET_FLAG('S', ret & 0b10000000)
        self.SET_FLAG('Z', ret == 0x00)
        self.SET_FLAG('5', ret & 0b00100000)
        self.SET_FLAG('H', (ret & HM) + (n & HM) > HM)
        self.SET_FLAG('3', ret & 0b00001000)
        self.SET_FLAG('V', n == 0x80)
        self.SET_FLAG('N', True)
        return ret

    # 16 bit arithmetic
    def INC_PC(self, n=1):
        """ PC <- PC + n """
        assert_n(n)
        self.PC = (self.PC + n) % CPU.MEMSIZE

    def INC_SP(self, n=1):
        """ SP <- SP + n """
        assert_n(n)
        self.SP = (self.SP + n) % CPU.MEMSIZE

    def DEC_SP(self, n=1):
        """ SP <- SP - n """
        assert_n(n)
        self.SP = (self.SP - n) % CPU.MEMSIZE

    def INC_ii(self, ii, n=1):
        """ ii <- ii + n"""
        assert_aa(ii)
        value = self.GET_ii(ii)
        value = (value + n) % CPU.MEMSIZE
        self.LD_ii_nn(ii, value)

    def DEC_ii(self, ii, n=1):
        """ ii <- ii - n"""
        assert_aa(ii)
        value = self.GET_ii(ii)
        value = (value - n) % CPU.MEMSIZE
        self.LD_ii_nn(ii, value)

    def ADD_ii_nn(self, ii, nn, carry=0):
        assert_aa(ii)
        assert_nn(nn)
        mm = self.GET_ii(ii)
        res = mm + nn + carry
        res_modulo = res % 0x10000
        self.LD_ii_nn(ii, res_modulo)
        HM = 0b0000111111111111
        self.SET_FLAG('H', (mm & HM) + (nn & HM) + carry > HM)
        self.SET_FLAG('C', res > 0x10000)

    def SUB_ii_nn(self, ii, nn, carry=0):
        assert_nn(nn)
        self.ADD_ii_nn(ii, (0x10000 - nn) % 0x10000, carry)

    # rotate and shift
    def shift_left_n(self, n, method):
        """ Bits of n are shifted left by one position.
            Bit 7 is copied to flag C.
            If method is 'RLC' bit 7 is also copied to 0.
            If method is 'RL' the old value of C is copied to bit 0.
            If method is 'SLA' bit 0 is unset.
            Returns new value.
        """
        assert_n(n)
        MSB = 0b10000000
        carry = 1 if (MSB & n) else 0
        if method == 'RLC':
            n = (n << 1) | carry
        elif method == 'RL':
            n = (n << 1) | self.GET_FLAG('C')
        elif method == 'SLA':
            n = (n << 1)
        else:
            raise ValueError('Invalid cycle type ' + str(method))
        self.SET_FLAG('S', n & 0b10000000)
        self.SET_FLAG('Z', n == 0x00)
        self.SET_FLAG('5', False)
        self.SET_FLAG('H', False)
        self.SET_FLAG('3', False)
        self.SET_FLAG('P', parity(n))
        self.SET_FLAG('N', False)
        self.SET_FLAG('C', carry)
        return n

    def shift_right_n(self, n, method):
        """ Bits of n are shifted right by one position.
            Bit 0 is copied to flag C.
            If method is 'RRC' bit 0 is also copied to 7.
            If method is 'RR' the old value of C is copied to bit 7.
            If method is 'SRL' bit 7 is unset.
            If method is 'SRA' bit 7 is not changed.
            Returns new value.
        """
        assert_n(n)
        LSB = 0b00000001
        MSB = 0b10000000
        carry = MSB if (LSB & n) else 0
        if method == 'RRC':
            n = (n >> 1) | carry
        elif method == 'RR':
            n = (n >> 1) | (self.GET_FLAG('C') << 7)
        elif method == 'SRL':
            n = (n >> 1)
        elif method == 'SRA':
            n = (n >> 1) | (n & MSB)
        else:
            raise ValueError('Invalid cycle type ' + str(method))
        self.SET_FLAG('S', n & 0b10000000)
        self.SET_FLAG('Z', n == 0x00)
        self.SET_FLAG('5', False)
        self.SET_FLAG('H', False)
        self.SET_FLAG('3', False)
        self.SET_FLAG('P', parity(n))
        self.SET_FLAG('N', False)
        self.SET_FLAG('C', carry)
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
        a = self.GET_A()
        LSB = 0b00001111
        MSB = 0b11110000
        la = a & LSB
        a = (a & MSB) | ((n & MSB) >> 4)
        n = (n << 4) | la
        self.LD_A_n(a)
        self.SET_FLAG('S', a & 0b10000000)
        self.SET_FLAG('Z', a == 0x00)
        self.SET_FLAG('5', False)
        self.SET_FLAG('H', False)
        self.SET_FLAG('3', False)
        self.SET_FLAG('P', parity(a))
        self.SET_FLAG('N', False)
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
        a = self.GET_A()
        LSB = 0b00001111
        MSB = 0b11110000
        la = a & LSB
        a = (a & MSB) | (n & LSB)
        n = (n >> 4) | (la << 4)
        self.LD_A_n(a)
        self.SET_FLAG('S', a & 0b10000000)
        self.SET_FLAG('Z', a == 0x00)
        self.SET_FLAG('5', False)
        self.SET_FLAG('H', False)
        self.SET_FLAG('3', False)
        self.SET_FLAG('P', parity(a))
        self.SET_FLAG('N', False)
        return n
