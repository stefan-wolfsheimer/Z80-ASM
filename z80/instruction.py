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

import abc


class Instruction(object):
    r_code = {'A': 0b111,
              'B': 0b000,
              'C': 0b001,
              'D': 0b010,
              'E': 0b011,
              'H': 0b100,
              'L': 0b101}
    dd_code = {'BC': 0b00,
               'DE': 0b01,
               'HL': 0b10,
               'SP': 0b11}
    qq_code = {'BC': 0b00,
               'DE': 0b01,
               'HL': 0b10,
               'AF': 0b11}
    index_code = {'IX': 0xdd,
                  'IY': 0xfd}

    @abc.abstractmethod
    def step(self, cpu):
        pass

    @staticmethod
    @abc.abstractmethod
    def register(instruction_set):
        raise NotImplementedError('Implement registration method.')

    def __init__(self):
        self.size = 0
