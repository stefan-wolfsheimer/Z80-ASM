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
from z80.instr_template_expansion import scan_asm
from z80.instr_template_expansion import extract_register_codes
from z80.instr_template_expansion import enum_register_codes
from z80.instr_template_expansion import expand_template


class TestInstructionSet(unittest.TestCase):
    def test_scan_instruction(self):
        self.assertEqual(scan_asm('EXX'), ('EXX',))
        self.assertEqual(scan_asm('EXX  '), ('EXX',))
        self.assertEqual(scan_asm('  EXX '), ('EXX',))
        self.assertEqual(scan_asm('  A  B '), ('A', 'B'))
        self.assertEqual(scan_asm('  A  B , C '), ('A', 'B', 'C'))

    def test_extract_register_codes(self):
        self.assertEqual(extract_register_codes(('EXX',)),
                         ((), 'EXX'))
        self.assertEqual(extract_register_codes(('INC', 'A')),
                         ((), 'INC', 'A'))
        self.assertEqual(extract_register_codes(('LD', 'A', 'n')),
                         ((), 'LD', 'A', 'n'))
        self.assertEqual(extract_register_codes(('LD', 'A', '( ii + d )')),
                         (('ii',), 'LD', 'A', '( {0} + d )'))
        self.assertEqual(extract_register_codes(('LD', 'r', 'r')),
                         (('r', 'r'), 'LD', '{0}', '{1}'))

    def test_enum_registers_codes(self):
        def unary(cpu):
            pass

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

    def test_expand_template_with_no_regs(self):
        result = ""
        for entry in expand_template(("LD A, I",
                                      (0xed, 0x57),
                                      1,
                                      "A <- I",
                                      lambda cpu: cpu)):
            result = entry['func'](entry['instr'])
        self.assertEqual(result, ('LD', 'A', 'I'))

    def test_expand_template_with_regs(self):
        result = {}
        for entry in expand_template(("LD r, (ii + d)",
                                      ("11{1}101", "01{0}110", "d"),
                                      1,
                                      "{0} <- ({1}+d)",
                                      lambda cpu, rr, ii: (rr, ii, cpu))):
            (rr, ii, cpu) = entry['func'](entry['instr'])
            if rr not in result:
                result[rr] = {}
            result[rr][ii] = cpu
        self.assertEqual(result,
                         {'A': {'IX': ('LD', 'A', '(IX + d)'),
                                'IY': ('LD', 'A', '(IY + d)')},
                          'B': {'IX': ('LD', 'B', '(IX + d)'),
                                'IY': ('LD', 'B', '(IY + d)')},
                          'C': {'IX': ('LD', 'C', '(IX + d)'),
                                'IY': ('LD', 'C', '(IY + d)')},
                          'D': {'IX': ('LD', 'D', '(IX + d)'),
                                'IY': ('LD', 'D', '(IY + d)')},
                          'E': {'IX': ('LD', 'E', '(IX + d)'),
                                'IY': ('LD', 'E', '(IY + d)')},
                          'H': {'IX': ('LD', 'H', '(IX + d)'),
                                'IY': ('LD', 'H', '(IY + d)')},
                          'L': {'IX': ('LD', 'L', '(IX + d)'),
                                'IY': ('LD', 'L', '(IY + d)')}})


if __name__ == '__main__':
    unittest.main()
