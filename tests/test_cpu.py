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
import unittest
import pytest
from z80.cpu import CPU


class TestCPU(unittest.TestCase):
    @pytest.mark.skip()
    def test_fetch_one_byte_instr(self):
        cpu = CPU()
        cpu.LD_ref_nn_n(0x0000, 0x0a)
        instr = cpu.fetch()
        self.assertEqual(instr.instr, ('LD', 'A', '(BC)'))

    @pytest.mark.skip()
    def test_fetch_two_bytes_instr(self):
        # todo fix this
        cpu = CPU()
        cpu.LD_ref_nn_n(0x0000, 0xdd)
        cpu.LD_ref_nn_n(0x0001, 0x36)
        instr = cpu.fetch()
        self.assertEqual(instr.instr, ('LD', '(IX + d)', 'n'))

    @pytest.mark.skip()
    def test_fetch_invalid_two_byte_instr_returns_nop(self):
        cpu = CPU()
        cpu.LD_ref_nn_n(0x0000, 0xdd)
        cpu.LD_ref_nn_n(0x0001, 0x01)
        instr = cpu.fetch()
        self.assertIsNone(instr)

    # 8 bit load #
    def test_LD_r_n(self):
        cpu = CPU()
        cpu.LD_r_n('B', 0x01)
        cpu.LD_r_n('C', 0x02)
        cpu.LD_r_n('D', 0x03)
        cpu.LD_r_n('E', 0x04)
        cpu.LD_r_n('H', 0x05)
        cpu.LD_r_n('L', 0x06)
        cpu.LD_r_n('A', 0x07)
        self.assertEqual(cpu['A'], 0x07)
        self.assertEqual(cpu['B'], 0x01)
        self.assertEqual(cpu['C'], 0x02)
        self.assertEqual(cpu['D'], 0x03)
        self.assertEqual(cpu['E'], 0x04)
        self.assertEqual(cpu['H'], 0x05)
        self.assertEqual(cpu['L'], 0x06)
        self.assertEqual(cpu['A'], 0x07)
        self.assertEqual(cpu.GET_ii('BC'), 0x0102)
        self.assertEqual(cpu.GET_ii('DE'), 0x0304)
        self.assertEqual(cpu.GET_ii('HL'), 0x0506)
        self.assertEqual(cpu.GET_ii('AF'), 0x0700)
        with self.assertRaises(ValueError):
            cpu.LD_r_n('X', 0x07)
        for r in "BCDEHLA":
            with self.assertRaises(ValueError):
                cpu.LD_r_n(r, 0x100)

    def test_LD_r__HL_(self):
        cpu = CPU()
        cpu.LD_r__HL_('A')
        self.assertEqual(cpu['A'], 0x00)
        cpu[0xa1b2] = 0x42
        cpu['HL'] = 0xa1b2
        self.assertEqual(cpu['H'], 0xa1)
        self.assertEqual(cpu['L'], 0xb2)
        cpu.LD_r__HL_('H')
        self.assertEqual(cpu['H'], 0x42)

    def test_LD_r__ii_d_(self):
        cpu = CPU()
        cpu['IX'] = 0x1012
        cpu['IY'] = 0xffff
        cpu[0x1013] = 0xff
        cpu[0x0001] = 0x10
        cpu.LD_r__ii_d_('D', 'IX', 1)
        cpu.LD_r__ii_d_('E', 'IY', 2)
        self.assertEqual(cpu['D'], 0xff)
        self.assertEqual(cpu['E'], 0x10)

    # ######################################################3
    # 8 bit getter
    @pytest.mark.skip()
    def test_GET_ref_index_plus_d(self):
        cpu = CPU()
        cpu.LD_IX_nn(0xfffd)
        cpu.LD_ref_nn_n(0x0000, 0x10)
        cpu.LD_ref_nn_n(0x0001, 0x00)
        cpu.LD_ref_nn_n(0x0002, 0x00)
        cpu.LD_ref_nn_n(0x0003, 0x03)
        cpu.LD_PC_nn(0x0001)
        self.assertEqual(cpu.GET_ref_index_plus_d('IX'), 0x10)

    # 16 bit getter
    @pytest.mark.skip()
    def test_GET_ii(self):
        cpu = CPU()
        cpu.LD_r_n('B', 0x20)
        cpu.LD_r_n('C', 0x22)
        cpu.LD_r_n('D', 0x30)
        cpu.LD_r_n('E', 0x32)
        cpu.LD_r_n('H', 0x40)
        cpu.LD_r_n('L', 0x42)
        cpu.LD_r_n('A', 0x50)
        cpu.LD_F_n(0x52)
        cpu.LD_PC_nn(0x6062)
        cpu.LD_SP_nn(0x7072)
        cpu.LD_IX_nn(0x8082)
        cpu.LD_IY_nn(0x9092)
        self.assertEqual(cpu.GET_ii('BC'), 0x2022)
        self.assertEqual(cpu.GET_ii('DE'), 0x3032)
        self.assertEqual(cpu.GET_ii('HL'), 0x4042)
        self.assertEqual(cpu.GET_ii('AF'), 0x5052)
        self.assertEqual(cpu.GET_ii('PC'), 0x6062)
        self.assertEqual(cpu.GET_ii('SP'), 0x7072)
        self.assertEqual(cpu.GET_ii('IX'), 0x8082)
        self.assertEqual(cpu.GET_ii('IY'), 0x9092)

    @pytest.mark.skip()
    def test_GET_ii_plus_d(self):
        cpu = CPU()
        self.assertEqual(cpu.GET_ii_plus_d('PC', -2), 0xfffe)
        self.assertEqual(cpu.GET_ii_plus_d('PC', 0), 0x0000)
        self.assertEqual(cpu.GET_ii_plus_d('PC', 1), 0x0001)
        self.assertEqual(cpu.GET_ii_plus_d('PC', 2), 0x0002)
        cpu.LD_PC_nn(0xffff)
        self.assertEqual(cpu.GET_ii_plus_d('PC', -1), 0xfffe)
        self.assertEqual(cpu.GET_ii_plus_d('PC', 1), 0x0000)
        self.assertEqual(cpu.GET_ii_plus_d('PC', 2), 0x0001)
        self.assertEqual(cpu.GET_ii_plus_d('PC', 3), 0x0002)

    @pytest.mark.skip()
    def test_GET_ref2_nn(self):
        cpu = CPU()
        cpu.LD_ref_nn_n(0xffff, 0x11)
        cpu.LD_ref_nn_n(0x0000, 0x22)
        cpu.LD_ref_nn_n(0x0001, 0x33)
        self.assertEqual(cpu.GET_ref2_nn(0x0000), 0x3322)
        self.assertEqual(cpu.GET_ref2_nn(0xffff), 0x2211)

    # 16 bit load
    @pytest.mark.skip()
    def test_GET_ref2_PC_plus_d(self):
        cpu = CPU()
        cpu.LD_ref_nn_n(0xffff, 0x11)
        cpu.LD_ref_nn_n(0x0000, 0x22)
        cpu.LD_ref_nn_n(0x0001, 0x33)
        cpu.LD_PC_nn(0xfffe)
        self.assertEqual(cpu.GET_ref2_PC_plus_d(0), 0x1100)
        self.assertEqual(cpu.GET_ref2_PC_plus_d(1), 0x2211)
        self.assertEqual(cpu.GET_ref2_PC_plus_d(2), 0x3322)

    @pytest.mark.skip()
    def test_LD_PC_nn(self):
        cpu = CPU()
        with self.assertRaises(ValueError):
            cpu.LD_PC_nn(0x10000)
        self.assertEqual(cpu.GET_PC(), 0x0000)

    @pytest.mark.skip()
    def test_LD_SP_nn(self):
        cpu = CPU()
        with self.assertRaises(ValueError):
            cpu.LD_SP_nn(0x10000)
        self.assertEqual(cpu.GET_SP(), 0x0000)

    # flags
    @pytest.mark.skip()
    def flags2str(self, flags, V_or_P='V'):
        ret = ''
        if V_or_P == 'V':
            sflags = 'SZ5H3VNC'
        else:
            sflags = 'SZ5H3PNC'
        for f in sflags:
            if f in flags and flags[f]:
                ret += f
        return ret

    @pytest.mark.skip()
    def test_SET_FLAGS(self):
        cpu = CPU()
        flags = {'S': False,
                 'Z': False,
                 '5': False,
                 'H': False,
                 '3': False,
                 'P': False,
                 'N': False,
                 'C': False}
        for f in flags:
            self.assertFalse(cpu.GET_FLAG(f))
        for f in flags.keys():
            cpu.SET_FLAG(f, True)
            v = cpu.GET_F()
            cpu.SET_FLAG(f, True)
            flags[f] = True
            self.assertEqual(v, cpu.GET_F())
            self.assertEqual(self.flags2str(flags, 'P'), cpu.GET_FLAGS('P'))
        keys = list(flags.keys())
        for f in keys[::-1]:
            cpu.SET_FLAG(f, False)
            v = cpu.GET_F()
            cpu.SET_FLAG(f, False)
            flags[f] = False
            self.assertEqual(v, cpu.GET_F())
            self.assertEqual(self.flags2str(flags, 'P'), cpu.GET_FLAGS('P'))
        for f in flags:
            self.assertFalse(cpu.GET_FLAG(f))

    @pytest.mark.skip()
    def test_SET_b_r(self):
        cpu = CPU()
        cpu.SET_b_r(1, 'A')
        self.assertEqual(2, cpu.GET_A())
        cpu.SET_b_r(7, 'A')
        self.assertEqual(0x82, cpu.GET_A())
        cpu.SET_b_r(1, 'A', 0)
        self.assertEqual(0x80, cpu.GET_A())

    @pytest.mark.skip()
    def test_SET_b_ref_nn(self):
        cpu = CPU()
        cpu.SET_b_ref_nn(1, 0x0010)
        self.assertEqual(2, cpu.GET_ref_nn(0x0010))
        cpu.SET_b_ref_nn(7, 0x0010)
        self.assertEqual(0x82, cpu.GET_ref_nn(0x0010))
        cpu.SET_b_ref_nn(1, 0x0010, 0)
        self.assertEqual(0x80, cpu.GET_ref_nn(0x0010))

    @pytest.mark.skip()
    def test_BIT_b_n(self):
        cpu = CPU()
        cpu.BIT_b_n(0, 0b01001011)
        self.assertEqual(0, cpu.GET_FLAG('Z'))
        cpu.BIT_b_n(7, 0b01001011)
        self.assertEqual(1, cpu.GET_FLAG('Z'))
        cpu.BIT_b_n(3, 0b01001011)
        self.assertEqual(0, cpu.GET_FLAG('Z'))

    # 8 bit arithmetic
    @pytest.mark.skip()
    def test_ADD_A_n(self):
        # todo add more edge cases
        tests = [(0x00, 0x40, False, 0x40, '')]
        cpu = CPU()
        for t in tests:
            cpu.LD_F_n(0x00)
            cpu.LD_A_n(t[0])
            cpu.SET_FLAG('C', t[2])
            cpu.ADD_A_n(t[1])
            self.assertEqual(cpu.GET_A(), t[3])
            self.assertEqual(cpu.GET_FLAGS('V'), t[4])

    @pytest.mark.skip()
    def test_SUB_A_n(self):
        # todo add more edge cases
        tests = [(0x40, 0x40, False, 0x00, 'Z')]
        cpu = CPU()
        for t in tests:
            cpu.LD_F_n(0x00)
            cpu.LD_A_n(t[0])
            cpu.SET_FLAG('C', t[2])
            cpu.SUB_A_n(t[1])
            self.assertEqual(cpu.GET_A(), t[3])
            self.assertEqual(cpu.GET_FLAGS('V'), t[4])

    @pytest.mark.skip()
    def test_AND_A_n(self):
        # todo add more edge cases
        tests = [(0x00, 0x00, 0x00, 'ZHP')]
        cpu = CPU()
        for t in tests:
            cpu.LD_F_n(0x00)
            cpu.LD_A_n(t[0])
            cpu.AND_A_n(t[1])
            self.assertEqual(cpu.GET_A(), t[2])
            self.assertEqual(cpu.GET_FLAGS('P'), t[3])

    @pytest.mark.skip()
    def test_OR_A_n(self):
        # todo add more edge cases
        tests = [(0x00, 0x00, 0x00, 'ZHP')]
        cpu = CPU()
        for t in tests:
            cpu.LD_F_n(0x00)
            cpu.LD_A_n(t[0])
            cpu.OR_A_n(t[1])
            self.assertEqual(cpu.GET_A(), t[2])
            self.assertEqual(cpu.GET_FLAGS('P'), t[3])

    @pytest.mark.skip()
    def test_XOR_A_n(self):
        # todo add more edge cases
        tests = [(0x00, 0x00, 0x00, 'ZHP')]
        cpu = CPU()
        for t in tests:
            cpu.LD_F_n(0x00)
            cpu.LD_A_n(t[0])
            cpu.XOR_A_n(t[1])
            self.assertEqual(cpu.GET_A(), t[2])
            self.assertEqual(cpu.GET_FLAGS('P'), t[3])

    @pytest.mark.skip()
    def test_CP_A_n(self):
        # todo add more edge cases
        tests = [(0x00, 0x00, 'ZN')]
        cpu = CPU()
        for t in tests:
            cpu.LD_F_n(0x00)
            cpu.LD_A_n(t[0])
            cpu.CP_A_n(t[1])
            self.assertEqual(cpu.GET_A(), t[0])
            self.assertEqual(cpu.GET_FLAGS('V'), t[2])

    @pytest.mark.skip()
    def test_INC_n(self):
        # todo add more edge cases
        tests = [(0x00, 0x01, '')]
        cpu = CPU()
        for t in tests:
            cpu.LD_F_n(0x00)
            n = cpu.INC_n(t[0])
            self.assertEqual(n, t[1])
            self.assertEqual(cpu.GET_FLAGS('V'), t[2])

    @pytest.mark.skip()
    def test_DEC_n(self):
        # todo add more edge cases
        tests = [(0x01, 0x00, 'ZN')]
        cpu = CPU()
        for t in tests:
            cpu.LD_F_n(0x00)
            n = cpu.DEC_n(t[0])
            self.assertEqual(n, t[1])
            self.assertEqual(cpu.GET_FLAGS('V'), t[2])

    # 16 bit arithmetic
    @pytest.mark.skip()
    def test_ADD_ii_nn(self):
        # todo add more edge cases
        tests = [(0x0000, 0x0000, 0, 0x00000, '')]
        cpu = CPU()
        for t in tests:
            cpu.LD_F_n(0x00)
            cpu.LD_ii_nn('HL', t[0])
            cpu.SET_FLAG('C', t[2])
            cpu.ADD_ii_nn('HL', t[1])
            self.assertEqual(cpu.GET_HL(), t[3])
            self.assertEqual(cpu.GET_FLAGS('V'), t[4])

    # increasing / decreasing registers
    @pytest.mark.skip()
    def test_INC_PC(self):
        cpu = CPU()
        cpu.LD_PC_nn(0xffff)
        cpu.INC_PC(2)
        self.assertEqual(cpu.GET_PC(), 0x0001)

    @pytest.mark.skip()
    def test_INC_SP(self):
        cpu = CPU()
        cpu.LD_SP_nn(0xffff)
        cpu.INC_SP(2)
        self.assertEqual(cpu.GET_SP(), 0x0001)

    @pytest.mark.skip()
    def test_DEC_SP(self):
        cpu = CPU()
        cpu.LD_SP_nn(0x0001)
        cpu.DEC_SP(2)
        self.assertEqual(cpu.GET_SP(), 0xffff)

    @pytest.mark.skip()
    def test_INC_ii(self):
        cpu = CPU()
        cpu.LD_ii_nn('DE', 0xffff)
        cpu.INC_ii('DE')
        self.assertEqual(cpu.GET_DE(), 0x0000)

    @pytest.mark.skip()
    def test_DEC_ii(self):
        cpu = CPU()
        cpu.LD_ii_nn('BC', 0x0000)
        cpu.DEC_ii('BC')
        self.assertEqual(cpu.GET_BC(), 0xffff)
        cpu.DEC_ii('BC')
        self.assertEqual(cpu.GET_BC(), 0xfffe)

    # rotate and shift
    @pytest.mark.skip()
    def test_RL(self):
        # todo add more edge cases
        tests = [(0x00, 0x00, 'ZP')]
        cpu = CPU()
        for t in tests:
            cpu.LD_F_n(0x00)
            self.assertEqual(cpu.shift_left_n(t[0], 'RL'), t[1])
            self.assertEqual(cpu.GET_FLAGS('P'), t[2])

    @pytest.mark.skip()
    def test_RLC(self):
        # todo add more edge cases
        tests = [(0x00, 0x00, 'ZP')]
        cpu = CPU()
        for t in tests:
            cpu.LD_F_n(0x00)
            self.assertEqual(cpu.shift_left_n(t[0], 'RLC'), t[1])
            self.assertEqual(cpu.GET_FLAGS('P'), t[2])

    @pytest.mark.skip()
    def test_SLA(self):
        # todo add more edge cases
        tests = [(0x00, 0x00, 'ZP')]
        cpu = CPU()
        for t in tests:
            cpu.LD_F_n(0x00)
            self.assertEqual(cpu.shift_left_n(t[0], 'SLA'), t[1])
            self.assertEqual(cpu.GET_FLAGS('P'), t[2])

    @pytest.mark.skip()
    def test_RR(self):
        # todo add more edge cases
        tests = [(0x00, 0x00, 'ZP')]
        cpu = CPU()
        for t in tests:
            cpu.LD_F_n(0x00)
            self.assertEqual(cpu.shift_right_n(t[0], 'RR'), t[1])
            self.assertEqual(cpu.GET_FLAGS('P'), t[2])

    @pytest.mark.skip()
    def test_RRC(self):
        # todo add more edge cases
        tests = [(0x00, 0x00, 'ZP')]
        cpu = CPU()
        for t in tests:
            cpu.LD_F_n(0x00)
            self.assertEqual(cpu.shift_right_n(t[0], 'RRC'), t[1])
            self.assertEqual(cpu.GET_FLAGS('P'), t[2])

    @pytest.mark.skip()
    def test_SRL(self):
        # todo add more edge cases
        tests = [(0x00, 0x00, 'ZP')]
        cpu = CPU()
        for t in tests:
            cpu.LD_F_n(0x00)
            self.assertEqual(cpu.shift_right_n(t[0], 'SRL'), t[1])
            self.assertEqual(cpu.GET_FLAGS('P'), t[2])

    @pytest.mark.skip()
    def test_SRA(self):
        # todo add more edge cases
        tests = [(0x00, 0x00, 'ZP')]
        cpu = CPU()
        for t in tests:
            cpu.LD_F_n(0x00)
            self.assertEqual(cpu.shift_right_n(t[0], 'SRA'), t[1])
            self.assertEqual(cpu.GET_FLAGS('P'), t[2])

    @pytest.mark.skip()
    def test_RLD(self):
        # todo add more edge cases
        tests = [(0x00, 0x00, 0x00, 0x00, 'ZP')]
        cpu = CPU()
        for t in tests:
            cpu.LD_F_n(0x00)
            cpu.LD_A_n(t[0])
            self.assertEqual(cpu.RLD_n(t[1]), t[3])
            self.assertEqual(cpu.GET_A(), t[2])
            self.assertEqual(cpu.GET_FLAGS('P'), t[4])

    @pytest.mark.skip()
    def test_RRD(self):
        # todo add more edge cases
        tests = [(0x00, 0x00, 0x00, 0x00, 'ZP')]
        cpu = CPU()
        for t in tests:
            cpu.LD_F_n(0x00)
            cpu.LD_A_n(t[0])
            self.assertEqual(cpu.RRD_n(t[1]), t[3])
            self.assertEqual(cpu.GET_A(), t[2])
            self.assertEqual(cpu.GET_FLAGS('P'), t[4])


if __name__ == '__main__':
    unittest.main()
