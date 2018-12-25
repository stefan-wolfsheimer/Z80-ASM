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
from z80.register import RegisterSet
from z80.register import IX
from z80.register import IY
from z80.register import PC
from z80.register import DE


class TestRegisterSet(unittest.TestCase):
    def test_register_plus_offset(self):
        self.assertEqual(PC(-2)(0x0000), 0xfffe)
        self.assertEqual(PC(0)(0x0000), 0x0000)
        self.assertEqual(PC(1)(0x0000), 0x0001)
        self.assertEqual(PC(2)(0x0000), 0x0002)
        self.assertEqual(PC(-1)(0xffff), 0xfffe)
        self.assertEqual(PC(1)(0xffff), 0x0000)
        self.assertEqual(PC(2)(0xffff), 0x0001)
        self.assertEqual(PC(3)(0xffff), 0x0002)

    def test_8bit_getter_register_plus_offset(self):
        reg = RegisterSet()
        reg['IX'] = 0x0001
        reg['IY'] = 0x0001
        reg['PC'] = 0x0001
        reg['DE'] = 0x0001
        reg[0x0000] = 0x10
        reg[0x0001] = 0x20
        reg[0x0002] = 0x30
        reg[0x0003] = 0x40
        self.assertEqual(reg[IX(-1)], 0x10)
        self.assertEqual(reg[IY(0)], 0x20)
        self.assertEqual(reg[PC(1)], 0x30)
        self.assertEqual(reg[DE(2)], 0x40)

    # #######
    # 16 bit
    # #######
    def test_16bit_getter_register_plus_offset(self):
        reg = RegisterSet()
        reg[0xffff] = 0x11
        reg[0x0000] = 0x22
        reg[0x0001] = 0x33
        reg['PC'] = 0xfffe
        self.assertEqual(reg.get16(PC(0)), 0x1100)
        self.assertEqual(reg.get16(PC(1)), 0x2211)
        self.assertEqual(reg.get16(PC(2)), 0x3322)

    def test_16bit_setter_register_plus_offset(self):
        reg = RegisterSet()
        reg['PC'] = 0xfffe
        reg.set16(PC(0), 0x1100)
        reg.set16(PC(1), 0x2211)
        reg.set16(PC(2), 0x3322)
        self.assertEqual(reg[0xffff], 0x11)
        self.assertEqual(reg[0x0000], 0x22)
        self.assertEqual(reg[0x0001], 0x33)

    # flags
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

    def test_SET_FLAGS(self):
        reg = RegisterSet()
        flags = {'S': False,
                 'Z': False,
                 '5': False,
                 'H': False,
                 '3': False,
                 'P': False,
                 'N': False,
                 'C': False}
        for f in flags:
            self.assertFalse(reg[f])
        for f in flags.keys():
            reg[f] = True
            v = reg['F']
            reg[f] = True
            flags[f] = True
            self.assertEqual(v, reg['F'])
            self.assertEqual(self.flags2str(flags, 'P'), reg.get_flags('P'))
        keys = list(flags.keys())
        for f in keys[::-1]:
            reg[f] = False
            v = reg['F']
            reg[f] = False
            flags[f] = False
            self.assertEqual(v, reg['F'])
            self.assertEqual(self.flags2str(flags, 'P'), reg.get_flags('P'))
        for f in flags:
            self.assertFalse(reg[f])


if __name__ == '__main__':
    unittest.main()
