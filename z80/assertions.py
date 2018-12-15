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


FLAGS = ('S', 'Z', '5', 'H', '3', 'P', 'V', 'N', 'C')


def assert_n(n):
    if not isinstance(n, int) or n < 0 or n > 0xff:
        raise ValueError("%s is not a byte" % str(n))


def assert_nn(nn):
    if not isinstance(nn, int) or nn < 0 or nn > 0xffff:
        raise ValueError("%s is not a word" % str(nn))


def assert_d(d):
    if not isinstance(d, int) or d < -0x80 or d > 0x7f:
        raise ValueError("%s is not a signed byte" % str(d))


def assert_q(q):
    if not isinstance(q, str) or q not in "BCDEHLAF":
        raise ValueError("Invalid register %s (not in BCDEHLAF)" % str(q))


def assert_r(r):
    if not isinstance(r, str) or r not in "BCDEHLA":
        raise ValueError("Invalid register %s (not in BCDEHLA)" % str(r))


def assert_b(b):
    if not isinstance(b, int) or b < 0 or b > 7:
        raise ValueError("Bit %s not in range [0, 7)" % str(b))


def assert_aa(ii):
    """ is any 16 bit register """
    pairs = ('BC', 'DE', 'HL', 'AF', 'SP', 'PC', 'IX', 'IY', 'IR')
    if not isinstance(ii, str) or ii not in pairs:
        raise ValueError("Invalid register pair %s" % str(ii))


def assert_dd(dd):
    pairs = ('BC', 'DE', 'HL', 'SP')
    if not isinstance(dd, str) or dd not in pairs:
        raise ValueError("Invalid register pair %s" % str(dd))


def assert_qq(qq):
    pairs = ('BC', 'DE', 'HL', 'AF')
    if not isinstance(qq, str) or qq not in pairs:
        raise ValueError("Invalid register pair %s" % str(qq))


def assert_ss(ss):
    pairs = ('BC', 'DE', 'HL', 'SP')
    if not isinstance(ss, str) or ss not in pairs:
        raise ValueError("Invalid register pair %s" % str(ss))


def assert_pp(pp):
    pairs = ('BC', 'DE', 'IX', 'SP')
    if not isinstance(pp, str) or pp not in pairs:
        raise ValueError("Invalid register pair %s" % str(pp))


def assert_rr(rr):
    pairs = ('BC', 'DE', 'IY', 'SP')
    if not isinstance(rr, str) or rr not in pairs:
        raise ValueError("Invalid register pair %s" % str(rr))


def assert_ii(index):
    """ is any index bit register """
    if not isinstance(index, str) or index not in ('IX', 'IY'):
        raise ValueError("Invalid index register %s" % str(index))


def assert_bcde(bcde):
    if not isinstance(bcde, str) or bcde not in ('BC', 'DE'):
        raise ValueError("Invalid register pair %s (expected BC or DE)" %
                         str(bcde))


def assert_flag(flag):
    if not isinstance(flag, str) or flag not in FLAGS:
        raise ValueError("Invalid flag pair %s ( expected %s)" %
                         (str(flag), ", ".join(FLAGS)))
