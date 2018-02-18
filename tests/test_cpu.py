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
        self.assertEqual(cpu.A, 0x07)
        self.assertEqual(cpu.B, 0x01)
        self.assertEqual(cpu.C, 0x02)
        self.assertEqual(cpu.D, 0x03)
        self.assertEqual(cpu.E, 0x04)
        self.assertEqual(cpu.H, 0x05)
        self.assertEqual(cpu.L, 0x06)
        self.assertEqual(cpu.A, 0x07)
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

    # arithmetic
    def test_INC_PC(self):
        cpu = CPU()
        cpu.LD_PC_nn(0xffff)
        cpu.INC_PC(2)
        self.assertEqual(cpu.GET_PC(), 0x0001)


if __name__ == '__main__':
    unittest.main()
