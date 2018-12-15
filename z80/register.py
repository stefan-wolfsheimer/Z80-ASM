from assertions import assert_aa
from assertions import assert_nn
from assertions import assert_n
from assertions import assert_d


MEMSIZE = 0x10000


class RegisterPlusOffset(object):
    def __init__(self, reg, d, memonic=None):
        assert_aa(reg)
        assert_d(d)
        self.reg = reg
        self.d = d
        self.memonic = memonic

    def offset(self, nn):
        assert_nn(nn)
        return (nn + self.d) % MEMSIZE

    def __str__(self):
        if self.memonic is None:
            return "({0} + {1})".format(self.reg, self.d)
        else:
            return self.memonic

    def len(self):
        return 1


class RegisterPlusOffset2(object):
    def __init__(self, reg, d, memonic=None):
        assert_aa(reg)
        assert_d(d)
        self.reg = reg
        self.d = d
        self.memonic = memonic

    def offset(self, nn):
        assert_nn(nn)
        return (nn + self.d) % MEMSIZE

    def __str__(self):
        if self.memonic is None:
            if self.d < 0:
                return "({0} - {1})".format(self.reg, self.d)
            else:
                return "({0} + {1})".format(self.reg, self.d)
        else:
            return self.memonic

    def len(self):
        return 2


def PC(d=0):
    return RegisterPlusOffset('PC', d)


def BC(d=0):
    return RegisterPlusOffset('BC', d)


def DE(d=0):
    return RegisterPlusOffset('DE', d)


def HL(d=0):
    return RegisterPlusOffset('HL', d)


class RegisterSet(object):
    FLAG_MASK = {'S': 0x80,
                 'Z': 0x40,
                 '5': 0x20,
                 'H': 0x10,
                 '3': 0x08,
                 'P': 0x04,
                 'V': 0x04,
                 'N': 0x02,
                 'C': 0x01}

    def __init__(self):
        self.main_register_set = {'B': 0x00, 'C': 0x00,
                                  'D': 0x00, 'E': 0x00,
                                  'H': 0x00, 'L': 0x00,
                                  'A': 0x00, 'F': 0x00,
                                  'I': 0x00, 'R': 0x00,
                                  'IX': 0x0000,
                                  'IY': 0x0000,
                                  'PC': 0x0000,
                                  'SP': 0x0000}
        self.alt_register_set = self.main_register_set.copy()
        self.mem = bytearray(MEMSIZE)

    def __getitem__(self, key):
        def get_reg_pair(p):
            return ((self.main_register_set[p[0]] << 8) +
                    (self.main_register_set[p[1]]))

        def get_reg_flag(f):
            if self.main_register_set['F'] & RegisterSet.FLAG_MASK[f]:
                return 1
            else:
                return 0

        if key in self.main_register_set:
            return self.main_register_set[key]
        elif key in ['BC', 'DE', 'HL', 'AF']:
            return get_reg_pair(key)
        elif key in ['IX', 'IY', 'SP', 'PC']:
            return self.main_register_set[key]
        elif key in RegisterSet.FLAG_MASK:
            get_reg_flag(key)
        elif isinstance(key, RegisterPlusOffset):
            return self.mem[key.offset(self[key.reg])]
        elif isinstance(key, int):
            assert_nn(key)
            return self.mem[key]
        else:
            raise KeyError('cannot access memory: ' + str(key))

    def __setitem__(self, key, value):
        if key in ['B', 'C', 'D', 'E', 'H', 'L', 'A', 'F', 'I', 'R']:
            assert_n(value)
            self.main_register_set[key] = value
        elif key in ['BC', 'DE', 'HL', 'AF', 'IR']:
            assert_nn(value)
            self.main_register_set[key[1]] = (value & 0x00ff)
            self.main_register_set[key[0]] = (value >> 8)
        elif key in ['IX', 'IY', 'SP', 'PC']:
            assert_nn(value)
            self.main_register_set[key] = value
        elif key in RegisterSet.FLAG_MASK:
            if value:
                self.main_register_set['F'] |= RegisterSet.FLAG_MASK[key]
            else:
                self.main_register_set['F'] &= (0xff ^
                                                RegisterSet.FLAG_MASK[key])
        elif isinstance(key, RegisterPlusOffset):
            assert_n(value)
            self.mem[key.offset(self[key.reg])] = value
        elif isinstance(key, int):
            assert_nn(key)
            assert_n(value)
            self.mem[key] = value
        else:
            raise KeyError('cannot access memory: ' + str(key))

    def __contains__(self, key):
        return \
            key in self.main_register_set or \
            key in RegisterSet.FLAG_MASK

    def swap(self):
        for r in "BCDEHLAFIR":
            v = self.main_register_set[r]
            self.main_register_set[r] = self.alt_register_set[r]
            self.alt_register_set = v
