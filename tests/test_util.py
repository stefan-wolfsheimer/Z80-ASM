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
import z80.util as util


class TestUntil(unittest.TestCase):
    def test_parity(self):
        self.assertTrue(util.parity(0x00))
        self.assertTrue(util.parity(0x03))
        self.assertTrue(util.parity(0xff))
        self.assertFalse(util.parity(0x01))
        self.assertFalse(util.parity(0x02))
        self.assertFalse(util.parity(0x04))
        self.assertFalse(util.parity(0x08))
        self.assertFalse(util.parity(0xfe))

    def test_n2d(self):
        self.assertEqual(util.n2d(0x00), 0)
        self.assertEqual(util.n2d(0x7f), 127)
        self.assertEqual(util.n2d(0x80), -128)
        self.assertEqual(util.n2d(0x81), -127)
        self.assertEqual(util.n2d(0xff), -1)


if __name__ == '__main__':
    unittest.main()
