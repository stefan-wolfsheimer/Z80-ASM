import os
import sys
sys.path.insert(0,
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from z80.instruction_set import InstructionSet


def main():
    instr_set = InstructionSet()
    for code1 in range(0, 0x100):
        if code1 in instr_set.instructions:
            if isinstance(instr_set.instructions[code1], dict):
                for code2 in range(0, 0x100):
                    if code2 in instr_set.instructions[code1]:
                        instr = instr_set.instructions[code1][code2]
                        cls_name = instr.__class__.__name__
                        print("{:02x} {:02x} {: <15} {}".format(code1,
                                                                code2,
                                                                instr.format(),
                                                                cls_name))
            else:
                instr = instr_set.instructions[code1]
                print("{:02x}    {: <15} {}".format(code1,
                                                    instr.format(),
                                                    instr.__class__.__name__))


if __name__ == "__main__":
    main()
