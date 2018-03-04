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
from z80.cpu import CPU


class TestCPU(unittest.TestCase):
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
        self.assertEqual(cpu.main_register_set.A, 0x07)
        self.assertEqual(cpu.main_register_set.B, 0x01)
        self.assertEqual(cpu.main_register_set.C, 0x02)
        self.assertEqual(cpu.main_register_set.D, 0x03)
        self.assertEqual(cpu.main_register_set.E, 0x04)
        self.assertEqual(cpu.main_register_set.H, 0x05)
        self.assertEqual(cpu.main_register_set.L, 0x06)
        self.assertEqual(cpu.main_register_set.A, 0x07)
        with self.assertRaises(ValueError):
            cpu.LD_r_n('X', 0x07)
        with self.assertRaises(ValueError):
            cpu.LD_r_n('A', 0x100)

    # 16 bit getter
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

    def test_GET_ref2_nn(self):
        cpu = CPU()
        cpu.LD_ref_nn_n(0xffff, 0x11)
        cpu.LD_ref_nn_n(0x0000, 0x22)
        cpu.LD_ref_nn_n(0x0001, 0x33)
        self.assertEqual(cpu.GET_ref2_nn(0x0000), 0x3322)
        self.assertEqual(cpu.GET_ref2_nn(0xffff), 0x2211)

    def test_GET_ref2_PC_plus_d(self):
        cpu = CPU()
        cpu.LD_ref_nn_n(0xffff, 0x11)
        cpu.LD_ref_nn_n(0x0000, 0x22)
        cpu.LD_ref_nn_n(0x0001, 0x33)
        cpu.LD_PC_nn(0xfffe)
        self.assertEqual(cpu.GET_ref2_PC_plus_d(0), 0x1100)
        self.assertEqual(cpu.GET_ref2_PC_plus_d(1), 0x2211)
        self.assertEqual(cpu.GET_ref2_PC_plus_d(2), 0x3322)

    # 16 bit load
    def test_LD_PC_nn(self):
        cpu = CPU()
        with self.assertRaises(ValueError):
            cpu.LD_PC_nn(0x10000)
        self.assertEqual(cpu.GET_PC(), 0x0000)

    def test_LD_SP_nn(self):
        cpu = CPU()
        with self.assertRaises(ValueError):
            cpu.LD_SP_nn(0x10000)
        self.assertEqual(cpu.GET_SP(), 0x0000)

    def test_LD_ii_nn(self):
        cpu = CPU()
        cpu.LD_ii_nn('BC', 0x1122)
        cpu.LD_ii_nn('DE', 0x3344)
        cpu.LD_ii_nn('HL', 0x5566)
        cpu.LD_ii_nn('SP', 0x7788)
        cpu.LD_ii_nn('PC', 0x99aa)
        cpu.LD_ii_nn('IX', 0xbbcc)
        cpu.LD_ii_nn('IY', 0xddee)
        cpu.LD_ii_nn('AF', 0xff01)
        self.assertEqual(cpu.GET_BC(), 0x1122)
        self.assertEqual(cpu.GET_DE(), 0x3344)
        self.assertEqual(cpu.GET_HL(), 0x5566)
        self.assertEqual(cpu.GET_SP(), 0x7788)
        self.assertEqual(cpu.GET_PC(), 0x99aa)
        self.assertEqual(cpu.GET_IX(), 0xbbcc)
        self.assertEqual(cpu.GET_IY(), 0xddee)
        self.assertEqual(cpu.GET_r('B'), 0x11)
        self.assertEqual(cpu.GET_r('C'), 0x22)
        self.assertEqual(cpu.GET_r('D'), 0x33)
        self.assertEqual(cpu.GET_r('E'), 0x44)
        self.assertEqual(cpu.GET_r('H'), 0x55)
        self.assertEqual(cpu.GET_r('L'), 0x66)
        self.assertEqual(cpu.GET_r('A'), 0xff)
        self.assertEqual(cpu.GET_F(), 0x01)

    # arithmetic
    def test_INC_PC(self):
        cpu = CPU()
        cpu.LD_PC_nn(0xffff)
        cpu.INC_PC(2)
        self.assertEqual(cpu.GET_PC(), 0x0001)

    def test_INC_SP(self):
        cpu = CPU()
        cpu.LD_SP_nn(0xffff)
        cpu.INC_SP(2)
        self.assertEqual(cpu.GET_SP(), 0x0001)

    def test_DEC_SP(self):
        cpu = CPU()
        cpu.LD_SP_nn(0x0001)
        cpu.DEC_SP(2)
        self.assertEqual(cpu.GET_SP(), 0xffff)


if __name__ == '__main__':
    unittest.main()
