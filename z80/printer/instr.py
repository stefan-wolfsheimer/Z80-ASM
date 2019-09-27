import json


class Printer(object):
    def write(self, groups):
        print(self.format(groups))

    def format(self, groups):
        raise NotImplementedError(self.__class__.__name__ + ".format")


class InstrJsonPrinter(Printer):
    def format(self, groups):
        return json.dumps(groups, indent=4)


class InstrPrettyPrinter(Printer):
    def format_instr(self, template, instr):
        def format_code(code):
            if isinstance(code, int):
                return "{:02x}".format(code)
            else:
                return "{:2}".format(str(code))

        fcodes = [format_code(code) for code in instr.get('opcode')]
        return "{:12} {: <15} {}".format(" ".join(fcodes),
                                         instr.get('assembler_str'), '')

    def format(self, groups):
        ret = ''
        for group in groups:
            if len(ret):
                ret += "\n"
            group_name = group.get('name')
            ret += "+-{}-+\n".format("-" * len(group_name))
            ret += "| {} |\n".format(group_name)
            ret += "+-{}-+\n".format("-" * len(group_name))
            for tmpl in group.get('templates'):
                assembler_str = tmpl.get('assembler_str')
                ret += "\n{0}\n{1}\n".format(assembler_str,
                                             "-" * len(assembler_str))
                for instr in tmpl.get('instructions'):
                    ret += self.format_instr(tmpl, instr) + "\n"
        return ret
