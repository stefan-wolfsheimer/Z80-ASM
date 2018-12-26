import os
import sys
sys.path.insert(0,
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from z80.cpu import INSTRUCTION_SET  # noqa: F402


def format_code(code):
    if isinstance(code, int):
        return "{:02x}".format(code)
    else:
        return "{:2}".format(code)


def list_instructions(instructions, codes=[]):
    if isinstance(instructions, dict):
        for k in sorted(instructions.keys()):
            list_instructions(instructions[k], codes + [k])
    else:
        fcodes = [format_code(code) for code in codes]
        print("{:12} {: <15} {}".format(" ".join(fcodes),
                                        instructions.format(), ""))


def main():
    list_instructions(INSTRUCTION_SET.instructions)


if __name__ == "__main__":
    main()
