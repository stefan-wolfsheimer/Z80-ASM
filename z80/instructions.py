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
# from z80.instructions import Instruction
import instr_templates as it
from instr_template_expansion import expand_template

from cpu import ALL_INSTRUCTIONS
from cpu import EIGHT_BIT_LOAD_GROUP
from cpu import SIXTEEN_BIT_LOAD_GROUP
from cpu import EXCHANGE_GROUP
from cpu import BLOCK_TRANSFER_GROUP
from cpu import SEARCH_GROUP
from cpu import EIGHT_BIT_ARITHMETIC_GROUP
from cpu import GENERAL_PURPOSE
from cpu import SIXTEEN_BIT_ARITHMETIC_GROUP
from cpu import ROTATE_AND_SHIFT_GROUP
from instruction import Instruction


def add_instruction_group(group, instr_set):
    grp = group.name
    for entry in instr_set:
        for expanded in expand_template(entry):
            instr = Instruction(assembler=expanded['instr'],
                                opcode=expanded['opcode'],
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


class InstructionSet(object):
    def __init__(self):
        self.instructions = ALL_INSTRUCTIONS.instructions

    def fetch(self, cpu):
        # todo 4 byte instructions
        code1 = cpu.GET_ref_PC_plus_d(0)
        if code1 in self.instructions:
            if isinstance(self.instructions[code1], dict):
                code2 = cpu.GET_ref_PC_plus_d(1)
                if code2 in self.instructions[code1]:
                    return self.instructions[code1][code2]
                else:
                    return None
            else:
                return self.instructions[code1]
        else:
            raise NotImplemented('instruction not implemented %02x' % code1)
