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
from z80.instructions import InstructionSet
from z80.cpu import CPU
import pytest


class TestInstructionSet(unittest.TestCase):
    def test_fetch_one_byte_instr(self):
        cpu = CPU()
        instr_set = InstructionSet()
        cpu.LD_ref_nn_n(0x0000, 0x0a)
        instr = instr_set.fetch(cpu)
        self.assertEqual(instr.instr, ('LD', 'A', '(BC)'))

    @pytest.mark.skip()
    def test_fetch_two_bytes_instr(self):
        # todo fix this
        cpu = CPU()
        instr_set = InstructionSet()
        cpu.LD_ref_nn_n(0x0000, 0xdd)
        cpu.LD_ref_nn_n(0x0001, 0x36)
        instr = instr_set.fetch(cpu)
        self.assertEqual(instr.instr, ('LD', '(IX + d)', 'n'))

    def test_fetch_invalid_two_byte_instr_returns_nop(self):
        cpu = CPU()
        instr_set = InstructionSet()
        cpu.LD_ref_nn_n(0x0000, 0xdd)
        cpu.LD_ref_nn_n(0x0001, 0x01)
        instr = instr_set.fetch(cpu)
        self.assertIsNone(instr)


if __name__ == '__main__':
    unittest.main()
