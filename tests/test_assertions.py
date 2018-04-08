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
import unittest
from z80.assertions import assert_n
from z80.assertions import assert_nn
from z80.assertions import assert_d
from z80.assertions import assert_q
from z80.assertions import assert_r
from z80.assertions import assert_b
from z80.assertions import assert_ii
from z80.assertions import assert_qq
from z80.assertions import assert_pp
from z80.assertions import assert_ss
from z80.assertions import assert_rr
from z80.assertions import assert_flag


class TestAssertions(unittest.TestCase):
    def test_assert_n(self):
        with self.assertRaises(ValueError):
            assert_n("X")
        with self.assertRaises(ValueError):
            assert_n(-1)
        with self.assertRaises(ValueError):
            assert_n(256)
        assert_n(34)

    def test_assert_nn(self):
        with self.assertRaises(ValueError):
            assert_nn("X")
        with self.assertRaises(ValueError):
            assert_nn(-1)
        with self.assertRaises(ValueError):
            assert_nn(0x10000)
        assert_nn(500)

    def test_assert_d(self):
        with self.assertRaises(ValueError):
            assert_d("X")
        with self.assertRaises(ValueError):
            assert_d(-129)
        with self.assertRaises(ValueError):
            assert_d(128)
        assert_d(127)
        assert_d(-128)

    def test_assert_q(self):
        assert_q('B')
        assert_q('C')
        assert_q('D')
        assert_q('E')
        assert_q('H')
        assert_q('L')
        assert_q('A')
        assert_q('F')

    def test_assert_r(self):
        with self.assertRaises(ValueError):
            assert_r("X")
        with self.assertRaises(ValueError):
            assert_r(1)
        assert_r('A')
        assert_r('B')
        assert_r('C')
        assert_r('D')
        assert_r('E')
        assert_r('H')
        assert_r('L')

    def test_assert_b(self):
        for i in range(0, 8):
            assert_b(i)
        with self.assertRaises(ValueError):
            assert_b(-1)
        with self.assertRaises(ValueError):
            assert_b(8)
        with self.assertRaises(ValueError):
            assert_b('0')

    def test_assert_ii(self):
        with self.assertRaises(ValueError):
            assert_ii("CD")
        with self.assertRaises(ValueError):
            assert_ii(1)
        assert_ii('BC')
        assert_ii('DE')
        assert_ii('HL')
        assert_ii('AF')
        assert_ii('SP')
        assert_ii('PC')
        assert_ii('IX')
        assert_ii('IY')
        assert_ii('IR')

    def test_assert_qq(self):
        assert_qq('BC')
        assert_qq('DE')
        assert_qq('HL')
        assert_qq('AF')

    def test_assert_ss(self):
        assert_ss('BC')
        assert_ss('DE')
        assert_ss('HL')
        assert_ss('SP')

    def test_assert_pp(self):
        assert_pp('BC')
        assert_pp('DE')
        assert_pp('IX')
        assert_pp('SP')

    def test_assert_rr(self):
        assert_rr('BC')
        assert_rr('DE')
        assert_rr('IY')
        assert_rr('SP')

    def test_assert_flag(self):
        assert_flag('S')
        assert_flag('Z')
        assert_flag('5')
        assert_flag('H')
        assert_flag('3')
        assert_flag('P')
        assert_flag('V')
        assert_flag('N')
        assert_flag('C')


if __name__ == '__main__':
    unittest.main()
