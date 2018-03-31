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
import z80.instr_templates as instr_templates
from z80.instr_template_expansion import expand_template


class Instruction(object):
    def __init__(self, instr, opcode, func, tstates=1, operation="", group=""):
        self.instr = instr
        self.opcode = opcode
        self.size = len(opcode)
        self.func = func
        self.tstates = tstates
        self.operation = operation
        self.fmt = instr[0]
        if len(instr[1:]) > 0:
            self.fmt += " " + ",".join(instr[1:])
        self.group = group

    def step(self, cpu):
        pass

    def format(self):
        return self.fmt


class InstructionSet(object):
    def __init__(self):
        self.instructions = {}
        self.add_instruction_group(instr_templates.EIGHT_BIT_LOAD_GROUP,
                                   "8 bit load group")
        self.add_instruction_group(instr_templates.SIXTEEN_BIT_LOAD_GROUP,
                                   "16 bit load group")
        self.add_instruction_group(instr_templates.EXCHANGE_GROUP,
                                   "exchange group")
        self.add_instruction_group(instr_templates.GENERAL_PURPOSE,
                                   "general purpose group")
        self.add_instruction_group(instr_templates.BLOCK_TRANSFER_GROUP,
                                   "block transfer group")

    def add_instruction_group(self, instr_set, grp):
        for entry in instr_set:
            for expanded in expand_template(entry):
                instr = Instruction(instr=expanded['instr'],
                                    opcode=expanded['opcode'],
                                    func=expanded['func'],
                                    tstates=expanded['tstates'],
                                    operation=expanded['operation'],
                                    group=grp)
                if len(instr.opcode) > 1 and isinstance(instr.opcode[1], int):
                    if instr.opcode[0] not in self.instructions:
                        self.instructions[instr.opcode[0]] = {}
                    self.instructions[instr.opcode[0]][instr.opcode[1]] = instr
                else:
                    self.instructions[instr.opcode[0]] = instr

    def fetch(self, cpu):
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
