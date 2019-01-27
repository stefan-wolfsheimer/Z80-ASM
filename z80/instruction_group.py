class InstructionGroup(object):
    def __init__(self, name, instruction_set):
        self.name = name
        self.instruction_templates = []
        self.instruction_set = instruction_set
        self.instruction_set.add_group(self)

    def add(self, instr_template):
        self.instruction_templates.append(instr_template)
        for instr in instr_template.instructions:
            self.instruction_set.add(instr)
