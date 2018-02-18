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
from z80.assertions import assert_r
from z80.assertions import assert_ii


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


if __name__ == '__main__':
    unittest.main()