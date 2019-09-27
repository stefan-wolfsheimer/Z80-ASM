from .instruction_set import InstructionSet
from .instruction_template import InstructionTemplate


class InstructionGroup(object):
    """
    A group of Instructions
    """
    def __init__(self, name: str,
                 instruction_set: InstructionSet,
                 short_name=None):
        """
        Constructs a InstructionGroup. Register it self
        to the InstructionSet

        Parameters
        ----------
        name : str
            The name of the group
        instruction_set: InstructionSet
            reference to the full InstructionSet
        short_name: string, optional
            The short name of the group, default value: name
        """
        self.name = name
        self.instruction_templates = []
        self.instruction_set = instruction_set
        self.instruction_set.add_group(self)
        self.short_name = name if short_name is None else short_name

    def add(self, instr_template: InstructionTemplate):
        self.instruction_templates.append(instr_template)
        for instr in instr_template.instructions:
            self.instruction_set.add(instr)

    def to_dict(self):
        ret = {'name': self.name,
               'short_name': self.short_name,
               'templates': [t.to_dict() for t in self.instruction_templates]}
        return ret
