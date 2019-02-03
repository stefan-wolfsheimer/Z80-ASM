import sys
from functools import partial
from cmd import Cmd
from .cpu import INSTRUCTION_SET


class BasicShell(Cmd):
    def __init__(self, *args, **kwargs):
        Cmd.__init__(self, *args, **kwargs)

    def completedefault(self, text, line, begin, end):
        args = line.split(None, 2)
        subshell = "{0}_shell".format(args[0])
        if hasattr(self, subshell):
            subshell = getattr(self, subshell)
            if len(args) == 1:
                return subshell.completenames('')
            elif len(args) == 2 and text:
                return subshell.completenames(args[1])
            elif len(args) >= 2 and hasattr(subshell,
                                            'complete_{0}'.format(args[1])):
                func = getattr(subshell,
                               'complete_{0}'.format(args[1]))
                return func(text, line, begin, end,
                            subline=line.split(None, 1)[1])
            else:
                return []
        else:
            return []

    def enter_subshell(self, shell, args):
        args = args.strip()
        if not args:
            shell.cmdloop()
        else:
            shell.onecmd(args)


class CpuShell(BasicShell):
    prompt = "z80/cpu> "

    def do_ls(self, args):
        pass

    def do_exit(self, args):
        return True


class InstrGroupShell(BasicShell):
    prompt = "z80/instr/group> "

    @staticmethod
    def enter(args, shell):
        shell.enter_subshell(shell, args)

    def __init__(self, group, *args, **kwargs):
        BasicShell.__init__(self, *args, **kwargs)
        self.group = group

    def do_exit(self, args):
        return True

    def cmdloop(self):
        InstrGroupShell.prompt = "z80/instr/" + self.group.short_name + "> "
        BasicShell.cmdloop(self)

    def do_ls(self, args):
        def format_code(code):
            if isinstance(code, int):
                return "{:02x}".format(code)
            else:
                return "{:2}".format(str(code))

        def list_instructions(instructions, codes=[]):
            if isinstance(instructions, dict):
                for k in instructions.keys():
                    list_instructions(instructions[k], codes + [k])
            else:
                fcodes = [format_code(code) for code in codes]
                print("{:12} {: <15} {}".format(" ".join(fcodes),
                                                instructions.format(), ""))
        for tmpl in self.group.instruction_templates:
            print("")
            print(tmpl.assembler_to_str())
            print("-" * len(tmpl.assembler_to_str()))
            for instr in tmpl.instructions:
                fcodes = [format_code(code) for code in instr.opcode]
                print("{:12} {: <15} {}".format(" ".join(fcodes),
                                                instr.assembler_to_str(), ""))


class InstrShell(BasicShell):
    prompt = "z80/instr> "

    @classmethod
    def add_group_commands(cls, groups):
        for group in groups:
            group_shell = InstrGroupShell(group)
            setattr(cls, group.short_name + "_shell", group_shell)
            setattr(cls, "do_" + group.short_name,
                    partial(InstrGroupShell.enter, **{'shell': group_shell}))

    def do_ls(self, args):
        for group in INSTRUCTION_SET.groups:
            print("")
            print("+" + "-" * (len(group.name) + 2) + "+")
            print("| " + group.name + " |")
            print("+" + "-" * (len(group.name) + 2) + "+")
            group_shell = getattr(self.__class__, group.short_name + "_shell")
            group_shell.do_ls(args)

    def complete_ls(self, text, line, begin, end, subline=None):
        # print("'{0}_{1}'".format(line, text))
        def complete_assembler(assembler, prefix):
            first = prefix[0]
            if len(prefix) == 1:
                if not first:
                    return sorted(assembler.keys())
                else:
                    return [f
                            for f in sorted(assembler.keys())
                            if f.startswith(first)]
            else:
                if first.startswith('(('):
                    first = first[1:]
                if first.endswith('))'):
                    first = first[:-1]
                if first in assembler:
                    return complete_assembler(assembler[first], prefix[1:])
                else:
                    return []

        if subline is None:
            subline = line
        args = subline.split()
        # fix: text is empty if line ends with '('
        # determine text manually
        if subline.endswith(' '):
            text = ''
        else:
            text = args[-1]
        if len(args) == 1:
            return complete_assembler(INSTRUCTION_SET.assembler, [''])
        else:
            if not text:
                args.append('')
            return complete_assembler(INSTRUCTION_SET.assembler, args[1:])
        return complete_assembler(INSTRUCTION_SET.assembler, text)

    def do_exit(self, args):
        return True


class Shell(BasicShell):
    prompt = "z80> "

    def __init__(self, *args, **kwargs):
        Cmd.__init__(self, *args, **kwargs)
        self.cpu_shell = CpuShell()
        self.instr_shell = InstrShell()

    def do_instr(self, args):
        self.enter_subshell(self.instr_shell, args)

    def do_cpu(self, args):
        self.enter_subshell(self.cpu_shell, args)

    def do_exit(self, args):
        return True


# Initialization
InstrShell.add_group_commands(INSTRUCTION_SET.groups)


if __name__ == "__main__":
    shell = Shell()
    if len(sys.argv) > 1:
        shell.onecmd(' '.join(sys.argv[1:]))
    else:
        shell.cmdloop()
