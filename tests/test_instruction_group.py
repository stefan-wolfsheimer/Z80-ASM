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
from z80.instruction_group import enum_register_codes
from z80.instruction_group import function_name_to_assembler


class TestInstructionSet(unittest.TestCase):
    def test_enum_registers_codes(self):
        self.assertEqual(enum_register_codes(()), [((), ())])
        self.assertEqual(sorted(enum_register_codes(('r',))),
                         [(('A', ), ('111', )),
                          (('B', ), ('000', )),
                          (('C', ), ('001', )),
                          (('D', ), ('010', )),
                          (('E', ), ('011', )),
                          (('H', ), ('100', )),
                          (('L', ), ('101', ))])
        self.assertEqual(sorted(enum_register_codes(('r', 'ii'))),
                         [(('A', 'IX'), ('111', '011')),
                          (('A', 'IY'), ('111', '111')),
                          (('B', 'IX'), ('000', '011')),
                          (('B', 'IY'), ('000', '111')),
                          (('C', 'IX'), ('001', '011')),
                          (('C', 'IY'), ('001', '111')),
                          (('D', 'IX'), ('010', '011')),
                          (('D', 'IY'), ('010', '111')),
                          (('E', 'IX'), ('011', '011')),
                          (('E', 'IY'), ('011', '111')),
                          (('H', 'IX'), ('100', '011')),
                          (('H', 'IY'), ('100', '111')),
                          (('L', 'IX'), ('101', '011')),
                          (('L', 'IY'), ('101', '111'))])

    def test_function_name_to_assembler(self):
        self.assertEqual(function_name_to_assembler('LD_r_r',
                                                    [('r', 'A'), ('r', 'B')]),
                         ['LD', 'A', 'B'])


if __name__ == '__main__':
    unittest.main()
