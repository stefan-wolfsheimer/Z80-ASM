import sys
from functools import partial
import argparse
from cmd import Cmd
from .cpu import INSTRUCTION_SET
from .printer.instr import InstrJsonPrinter
from .printer.instr import InstrPrettyPrinter


class ArgumentError(Exception):
    pass


class ArgumentParser(argparse.ArgumentParser):
    def exit(self, status=0, message=''):
        raise ArgumentError(message)


class InstrListArgumentParser(ArgumentParser):
    def __init__(self, *args, **kwargs):
        gr_name = kwargs.pop('group_name', None)
        kwargs['add_help'] = False
        if gr_name is None:
            kwargs['description'] = 'List all instructions'
        else:
            kwargs['description'] = 'List all instructions of ' + gr_name
        kwargs['usage'] = 'ls [OPTIONS]'
        super(InstrListArgumentParser, self).__init__(*args, **kwargs)
        self.add_argument('--json', action='store_true',
                          help="json format")


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
        self.parser_ls = InstrListArgumentParser(group_name=group.name)

    def do_exit(self, args):
        return True

    def cmdloop(self):
        InstrGroupShell.prompt = "z80/instr/" + self.group.short_name + "> "
        BasicShell.cmdloop(self)

    def help_ls(self):
        self.parser_ls.print_help()

    def do_ls(self, args):
        try:
            args = self.parser_ls.parse_args(args.split())
        except ArgumentError as e:
            sys.stderr.write(str(e))
            return

        if args.json:
            printer = InstrJsonPrinter()
        else:
            printer = InstrPrettyPrinter()
        printer.write([self.group.to_dict()])


class InstrShell(BasicShell):
    prompt = "z80/instr> "

    @classmethod
    def add_group_commands(cls, groups):
        for group in groups:
            group_shell = InstrGroupShell(group)
            setattr(cls, group.short_name + "_shell", group_shell)
            setattr(cls, "do_" + group.short_name,
                    partial(InstrGroupShell.enter, **{'shell': group_shell}))

    def __init__(self, *args, **kwargs):
        BasicShell.__init__(self, *args, **kwargs)
        self.parser_ls = InstrListArgumentParser()

    def do_ls(self, args):
        try:
            args = self.parser_ls.parse_args(args.split())
        except ArgumentError as e:
            sys.stderr.write(str(e))
            return
        if args.json:
            printer = InstrJsonPrinter()
        else:
            printer = InstrPrettyPrinter()
        printer.write([group.to_dict()
                       for group in INSTRUCTION_SET.groups])

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
