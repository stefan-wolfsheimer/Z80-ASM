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


def assert_n(n):
    if not isinstance(n, int) or n < 0 or n > 0xff:
        raise ValueError("%s is not a byte" % str(n))


def assert_nn(nn):
    if not isinstance(nn, int) or nn < 0 or nn > 0xffff:
        raise ValueError("%s is not a word" % str(nn))


def assert_d(d):
    if not isinstance(d, int) or d < -0x80 or d > 0x7f:
        raise ValueError("%s is not a signed byte" % str(d))


def assert_r(r):
    if not isinstance(r, str) or r not in "BCDEHLA":
        raise ValueError("Invalid register %s (not in BCDEHLA)" % str(r))


def assert_ii(ii):
    pairs = ('BC', 'DE', 'HL', 'AF', 'SP', 'PC', 'IX', 'IY', 'IR')
    if not isinstance(ii, str) or ii not in pairs:
        raise ValueError("Invalid register pair %s" % str(ii))


def assert_index(index):
    if not isinstance(index, str) or index not in ('IX', 'IY'):
        raise ValueError("Invalid index register %s" % str(index))


def assert_bcde(bcde):
    if not isinstance(bcde, str) or bcde not in ('BC', 'DE'):
        raise ValueError("Invalid register pair %s (expected BC or DE)" %
                         str(bcde))
