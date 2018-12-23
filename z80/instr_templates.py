# flake8: noqa
################################################################################
#
# 8 bit load group
#
################################################################################
EIGHT_BIT_LOAD_GROUP = [
    # ("LD r, r",        ("01{0}{1}"),                  1, "{0} <- {1}",      lambda c, r, rs: c.LD_r_n(r, c.GET_r(rs))),
    # ("LD r, n",        ("00{0}110", "n"),             1, "{0} <- n",        lambda c, r:     c.LD_r_n(r, c.GET_ref_PC_plus_d(1))),
    # ("LD r, (HL)",     ("01{0}110"),                  1, "{0} <- (HL)",     lambda c, r:     c.LD_r_n(r, c.GET_ref_HL())),
    # ("LD r, (ii + d)", ("11{1}101", "01{0}110", "d"), 1, "{0} <- ({1}+d)",  lambda c, r, i:  c.LD_r_n(r, c.GET_ref_index_plus_d(i))),
    # ("LD (HL), r",     ("01110{0}"),                  1, "(HL) <- {0}",     lambda c, r:     c.LD_ref_HL_n(c.GET_r(r))),
    # ("LD (HL), n",     (0x36, "n"),                   1, "(HL) <- n",       lambda c:        c.LD_ref_HL_n(c.GET_ref_PC_plus_d(1))),
    # ("LD (ii + d), r", ("11{0}101", "01110{1}", "d"), 1, "({0}+d) <- {1}",  lambda c, i, r:  c.LD_ref_index_plus_d(i, c.GET_r(r))),
    # ("LD (ii + d), n", ("11{0}101", 0x36, "d", "n"),  1, "({0}+d) <- n",    lambda c, i:     c.LD_ref_index_plus_d(i, c.GET_ref_PC_plus_d(3))),
    # ("LD A, (BC)",     (0x0a),                        1, "A <- (BC)",       lambda c:        c.LD_A_n(c.GET_ref_nn(c.GET_BC()))),
    # ("LD A, (DE)",     (0x1a),                        1, "A <- (DE)",       lambda c:        c.LD_A_n(c.GET_ref_nn(c.GET_DE()))),
    # ("LD A, (nn)",     (0x3a, "nl", "nh"),            1, "A <- (nn)",       lambda c:        c.LD_A_n(c.GET_ref_nn((c.GET_PC_plus_d(2) << 8) +
    #                                                                                                               c.GET_PC_plus_d(1)))),
    # ("LD (BC), A",     (0x02),                        1, "(BC) <- A",       lambda c:        c.LD_ref_nn_n(c.GET_BC(), c.GET_A())),
    # ("LD (DE), A",     (0x12),                        1, "(DE) <- A",       lambda c:        c.LD_ref_nn_n(c.GET_DE(), c.GET_A())),
    # ("LD (nn), A",     (0x32, "nl", "nh"),            1, "(nn) <- A",       lambda c:        c.LD_ref_nn_n((c.GET_PC_plus_d(2) << 8) +
    #                                                                                                       c.GET_PC_plus_d(1), c.GET_A())),
    # ("LD A, I",        (0xed, 0x57),                  1, "A <- I",          lambda c:        c.LD_A_n(c.GET_I())),
    # ("LD A, R",        (0xed, 0x5f),                  1, "A <- R",          lambda c:        c.LD_A_n(c.GET_R())),
    # ("LD I, A",        (0xed, 0x47),                  1, "I <- A",          lambda c:        c.LD_I_n(c.GET_A())),
    # ("LD R, A",        (0xed, 0x4f),                  1, "R <- A",          lambda c:        c.LD_R_n(c.GET_A()))
]

################################################################################
#
# 16 bit load group
#
################################################################################
SIXTEEN_BIT_LOAD_GROUP = [
#    ("LD dd, nn",      ("00{0}0001", "nl", "nh"),       1, "{0} <- nn",         lambda c, dd:  c.LD_dd_nn(dd, c.GET_ref2_PC_plus_d(1))),
#    ("LD ii, nn",      ("11{0}101", 0x21, "nl", "nh"),  1, "{0} <- nn",         lambda c, ii:  c.LD_index_nn(ii, c.GET_ref2_PC_plus_d(2))),
#    ("LD HL, (nn)",    (0x2a, "nl", "nh"),              1, "HL <- (nn)",        lambda c:      c.LD_dd_nn('HL', c.GET_ref2_PC_plus_d(1))),
#    ("LD dd, (nn)",    (0xed, "01{0}1011", "nl", "nh"), 1, "dd <- (nn)",        lambda c, dd:  c.LD_dd_nn(dd, c.GET_ref2_PC_plus_d(2))),
#    ("LD ii, (nn)",    ("11{0}101", 0x2a, "nl", "nh"),  1, "{0} <- (nn)",       lambda c, ii:  c.LD_ii_nn(ii, c.GET_ref2_PC_plus_d(2))),
#    ("LD (nn), HL",    (0x22, "nl", "nh"),              1, "(nn) <- HL,",       lambda c:      c.LD_ref_nn_nn(c.GET_ref2_PC_plus_d(1),
#                                                                                                              c.GET_HL())),
#    ("LD (nn), dd",    (0xed, "01{0}0011", "nl", "nh"), 1, "(nn) <- dd",        lambda c, dd: c.LD_ref_nn_nn(c.GET_ref2_PC_plus_d(2),
#                                                                                                             c.GET_ii(dd))),
#    ("LD (nn), ii",    ("11{0}101", 0x22, "nl", "nh"),  1, "nn <- {0}",         lambda c, ii: c.LD_ref_nn_nn(c.GET_ref2_PC_plus_d(2),
#                                                                                                             c.GET_ii(ii))),
#    ("LD SP, HL",      (0xf9),                          1, "SP <- HL",          lambda c:     c.LD_SP_nn(c.GET_HL())),
#    ("LD SP, ii",      ("11{0}101", 0xf9),              1, "SP <- {0}",         lambda c, ii: c.LD_SP_nn(c.GET_ii(ii))),
#    ("PUSH qq",        ("11{0}0101"),                   1, ("(SP-2) <- qq," +
#                                                           "SP <- SP-2"),      lambda c, qq: c.PUSH_qq(qq)),
#    ("PUSH ii",        ("11{0}101", 0xe5),              1, ("(SP-2) <- {0}, " +
#                                                            "SP <- SP-2"),      lambda c, ii: c.PUSH_ii(ii)),
#    ("POP qq",         ("11{0}0001"),                   1, ("qq <- (SP), " +
#                                                            "SP <- SP+2"),      lambda c, qq: c.POP_qq(qq)),
#    ("POP ii",         ("11{0}101", 0xe1),              1, ("{0} <- (SP)" +
#                                                            "SP <- SP+2"),      lambda c, ii: c.POP_ii(ii))
]

################################################################################
#
# exchange group
#
################################################################################
EXCHANGE_GROUP = [
    ("EX DE, HL",   (0xeb),             1, "DE <-> HL",                          lambda c: c.EX_DE_HL()),
    ("EX AF, AF'",  (0x08),             1, "AF <-> AF'",                         lambda c: c.EX_AF_altAF()),
    ("EXX",         (0xd9),             1, "BC <-> BC', DE <-> DE', HL <-> HL'", lambda c: c.EXX()),
    ("EX (SP), HL", (0xe3),             1, "H <-> (SP+1), L <-> (SP)",           lambda c: c.EX_ref_SP_HL()),
    ("EX (SP), ii", ("11{0}101", 0xe3), 1, "{0}_h <-> (SP+1), {0}_l <-> (SP)",   lambda c: c.EX_ref_SP_ii())]

################################################################################
#
# block transfer group
#
################################################################################
# todo: make t-states dynamic, depending on the result
# T-states for LDIR and LDDR: if BC = 0: 16
BLOCK_TRANSFER_GROUP = [
    ("LDI",  (0xed, 0xa0), 16, "(DE) <- (HL), DE <- DE + 1, HL <- HL + 1, BC <- BC - 1",               lambda c: c.LDI()),
    ("LDIR", (0xed, 0xb0), 21, "(DE) <- (HL), DE <- DE + 1, HL <- HL + 1, BC <- BC - 1 WHILE BC != 0", lambda c: c.LDIR()),
    ("LDD",  (0xed, 0xa8), 16, "(DE) <- (HL), DE <- DE - 1, HL <- HL - 1, BC <- BC - 1",               lambda c: c.LDD()),
    ("LDDR", (0xed, 0xb8), 21, "(DE) <- (HL), DE <- DE - 1, HL <- HL - 1, BC <- BC - 1 WHILE BC != 0", lambda c: c.LDDR())]

################################################################################
#
# Search group
#
################################################################################
# todo: make t-states dynamic, depending on the result
# T-states for CPIR and CPDR: if BC = 0 and A=(HL): 16
SEARCH_GROUP = [
    ("CPI",  (0xed, 0xa1), 16, "A - (HL), HL <- HL + 1, BC <- BC - 1", lambda c: c.CPI()),
    ("CPIR", (0xed, 0xb1), 21, "A - (HL), HL <- HL + 1, BC <- BC - 1", lambda c: c.CPIR()),
    ("CPD",  (0xed, 0xa9), 16, "A - (HL), HL <- HL - 1, BC <- BC - 1", lambda c: c.CPD()),
    ("CPDR", (0xed, 0xb9), 16, "A - (HL), HL <- HL - 1, BC <- BC - 1", lambda c: c.CPDR())]

################################################################################
#
# 8-bit arithmetic group
#
################################################################################
EIGHT_BIT_ARITHMETIC_GROUP = [
    ("ADD A, r",        ("10000{0}"),             4,  "A <- A + {0}",               lambda c, r: c.ADD_A_n(c.GET_r(r))),
    ("ADD A, n",        (0xc6, "n"),              7,  "A <- A + n",                 lambda c:    c.ADD_A_n(c.GET_ref_PC_plus_d(1))),
    ("ADD A, (HL)",     (0x86),                   7,  "A <- A + (HL)",              lambda c:    c.ADD_A_n(c.GET_ref_HL())),
    ("ADD A, (ii + d)", ("11{0}101", 0x86, "d"),  19, "A <- A + ({0}+d)",           lambda c, i: c.ADD_A_n(c.GET_ref_index_plus_d(i))),

    ("ADC A, r",        ("10001{0}"),             4,  "A <- A + {0} + CY",          lambda c, r: c.ADC_A_n(c.GET_r(r))),
    ("ADC A, n",        (0xce, "n"),              7,  "A <- A + n",                 lambda c:    c.ADC_A_n(c.GET_ref_PC_plus_d(1))),
    ("ADC A, (HL)",     (0x8e),                   7,  "A <- A + (HL)",              lambda c:    c.ADC_A_n(c.GET_ref_HL())),
    ("ADC A, (ii + d)", ("11{0}101", 0x8e, "d"),  19, "A <- A + ({0}+d)",           lambda c, i: c.ADC_A_n(c.GET_ref_index_plus_d(i))),

    ("SUB A, r",        ("10010{0}"),             4,  "A <- A - {0}",               lambda c, r: c.SUB_A_n(c.GET_r(r))),
    ("SUB A, n",        (0xd6, "n"),              7,  "A <- A - n",                 lambda c:    c.SUB_A_n(c.GET_ref_PC_plus_d(1))),
    ("SUB A, (HL)",     (0x96),                   7,  "A <- A - (HL)",              lambda c:    c.SUB_A_n(c.GET_ref_HL())),
    ("SUB A, (ii + d)", ("11{0}101", 0x96, "d"),  19, "A <- A - ({0}+d)",           lambda c, i: c.SUB_A_n(c.GET_ref_index_plus_d(i))),

    ("SBC A, r",        ("10011{0}"),             4,  "A <- A - {0} - CY",          lambda c, r: c.SBC_A_n(c.GET_r(r))),
    ("SBC A, n",        (0xde, "n"),              7,  "A <- A - n - CY",            lambda c:    c.SBC_A_n(c.GET_ref_PC_plus_d(1))),
    ("SBC A, (HL)",     (0x9e),                   7,  "A <- A - (HL) - CY",         lambda c:    c.SBC_A_n(c.GET_ref_HL())),
    ("SBC A, (ii + d)", ("11{0}101", 0x9e, "d"),  19, "A <- A - ({0}+d)",           lambda c, i: c.SBC_A_n(c.GET_ref_index_plus_d(i))),

    ("AND A, r",        ("10100{0}"),             4,  "A <- A AND {0}",             lambda c, r: c.AND_A_n(c.GET_r(r))),
    ("AND A, n",        (0xe6, "n"),              7,  "A <- A AND n",               lambda c:    c.AND_A_n(c.GET_ref_PC_plus_d(1))),
    ("AND A, (HL)",     (0xa6),                   7,  "A <- A AND (HL)",            lambda c:    c.AND_A_n(c.GET_ref_HL())),
    ("AND A, (ii + d)", ("11{0}101", 0xa6, "d"),  19, "A <- A AND ({0}+d)",         lambda c, i: c.AND_A_n(c.GET_ref_index_plus_d(i))),

    ("OR A, r",         ("10110{0}"),             4,  "A <- A OR {0}",              lambda c, r: c.OR_A_n(c.GET_r(r))),
    ("OR A, n",         (0xf6, "n"),              7,  "A <- A OR n",                lambda c:    c.OR_A_n(c.GET_ref_PC_plus_d(1))),
    ("OR A, (HL)",      (0xb6),                   7,  "A <- A OR (HL)",             lambda c:    c.OR_A_n(c.GET_ref_HL())),
    ("OR A, (ii + d)",  ("11{0}101", 0xb6, "d"),  19, "A <- A OR ({0}+d)",          lambda c, i: c.OR_A_n(c.GET_ref_index_plus_d(i))),

    ("XOR A, r",        ("10101{0}"),             4,  "A <- A XOR {0}",             lambda c, r: c.XOR_A_n(c.GET_r(r))),
    ("XOR A, n",        (0xee, "n"),              7,  "A <- A XOR n",               lambda c:    c.XOR_A_n(c.GET_ref_PC_plus_d(1))),
    ("XOR A, (HL)",     (0xae),                   7,  "A <- A XOR (HL)",            lambda c:    c.XOR_A_n(c.GET_ref_HL())),
    ("XOR A, (ii + d)", ("11{0}101", 0xae, "d"),  19, "A <- A XOR ({0}+d)",         lambda c, i: c.XOR_A_n(c.GET_ref_index_plus_d(i))),

    ("CP r",            ("10111{0}"),             4,  "A - {0}",                    lambda c, r: c.CP_A_n(c.GET_r(r))),
    ("CP n",            (0xfe, "n"),              7,  "A - n",                      lambda c:    c.CP_A_n(c.GET_ref_PC_plus_d(1))),
    ("CP (HL)",         (0xbe),                   7,  "A - (HL)",                   lambda c:    c.CP_A_n(c.GET_ref_HL())),
    ("CP (ii + d)",     ("11{0}101", 0xbe, "d"),  19, "A - ({0}+d)",                lambda c, i: c.CP_A_n(c.GET_ref_index_plus_d(i))),

    ("INC r",           ("00{0}100"),             4,  "{0} <- {0} + 1",             lambda c, r: c.LD_r_n(r, c.INC_n(c.GET_r(r)))),
    ("INC (HL)",        (0x34),                   11, "(HL) < (HL) + 1",            lambda c:    c.LD_ref_HL_n(c.INC_n(c.GET_ref_HL()))),
    ("INC (ii + d)",    ("11{0}101", 0x34, "d"),  23, "({0} + d) <- ({0} + d) + 1", lambda c, i: c.LD_ref_HL_n(c.INC_n(c.GET_ref_index_plus_d(i)))),

    ("DEC r",           ("00{0}101"),             4,  "{0} <- {0} + 1",             lambda c, r: c.LD_r_n(r, c.DEC_n(c.GET_r(r)))),
    ("DEC (HL)",        (0x35),                   11, "(HL) < (HL) + 1",            lambda c:    c.LD_ref_HL_n(c.DEC_n(c.GET_ref_HL()))),
    ("DEC (ii + d)",    ("11{0}101", 0x35, "d"),  23, "({0} + d) <- ({0} + d) + 1", lambda c, i: c.LD_ref_HL_n(c.DEC_n(c.GET_ref_index_plus_d(i))))]

################################################################################
#
# General purpose group
#
################################################################################
def NOP(cpu):
    pass

GENERAL_PURPOSE = [
    ("NOP", (0x00), 1, "", NOP)
]

################################################################################
#
# 16 bit arithmetic
#
################################################################################
def ADD_HL_ss(cpu, ss):
    cpu.ADD_ii_nn('HL', cpu.GET_ss(ss))

def ADC_HL_ss(cpu, ss):
    cpu.ADD_ii_nn('HL', cpu.GET_ss(ss), cpu.GET_FLAG('C'))

def SBC_HL_ss(cpu, ss):
    cpu.SUB_ii_nn('HL', cpu.GET_ss(ss), cpu.GET_FLAG('C'))

def ADD_IX_pp(cpu, pp):
    cpu.ADD_ii_nn('IX', cpu.GET_ii(pp))

def ADD_IY_rr(cpu, rr):
    cpu.ADD_ii_nn('IY', cpu.GET_ii(rr))

def INC_ss(cpu, ss):
    cpu.INC_ii(ss)

def INC_ii(cpu, ii):
    cpu.INC_ii(ii)

def DEC_ss(cpu, ss):
    cpu.DEC_ii(ss)

def DEC_ii(cpu, ii):
    cpu.DEC_ii(ii)

SIXTEEN_BIT_ARITHMETIC_GROUP = [
    ("ADD HL, ss", ("00{0}1001"),       11, "HL <- HL + {0}",      ADD_HL_ss),
    ("ADC HL, ss", (0xed, "01{0}1010"), 15, "HL <- HL + {0} + CY", ADC_HL_ss),
    ("SBC HL, ss", (0xed, "01{0}0010"), 15, "HL <- HL - {0} - CY", SBC_HL_ss),
    ("ADD IX, pp", (0xdd, "00{0}1001"), 15, "IX <- IX + {0}",      ADD_IX_pp),
    ("ADD IY, rr", (0xfd, "00{0}1001"), 15, "IY <- IY + {0}",      ADD_IY_rr),
#    ("INC ss",     ("00{0}0011"),        6, "{0} <- {0} + 1",      INC_ss),
#    ("INC ii",     ("11{0}101", 0x23),  10, "{0} <- {0} + 1",      INC_ii),
#    ("DEC ss",     ("00{0}1011"),        6, "{0} <- {0} - 1",      DEC_ss),
#    ("DEC ii",     ("11{0}101", 0x2b),  10, "{0} <- {0} - 1",      DEC_ii)
]

################################################################################
#
# rotate and shift group
#
################################################################################
ROTATE_AND_SHIFT_GROUP = [
    ("RLCA",       (0x07),                         4, "A0 << A7, CY << A",                   lambda c:    c.RLC_r('A')),
    ("RLA",        (0x17),                         4, "A0 << CY, CY << A",                   lambda c:    c.RL_r('A')),
    ("RRCA",       (0x0f),                         4, "A0 >> A7, A >> CY",                   lambda c:    c.RRC_r('A')),
    ("RRA",        (0x1f),                         4, "CY >> A7, A >> CY",                   lambda c:    c.RR_r('A')),

    ("RLC r",      (0xcb, "00000{0}"),             8, "{0}0 << {0}7, CY << {0}",             lambda c, r: c.RLC_r(r)),
    ("RLC (HL)",   (0xcb, 0x06),                  15, "(HL)0 << (HL)7, CY << (HL)",          lambda c:    c.RLC_ref_HL()),
    ("RLC (ii+d)", ("11{0}101", 0xcb, "d", 0x06), 23, "({0}+d)0 << ({0}+d)7, CY << ({0}+d)", lambda c, i: c.RLC_ref_index_plus_d(i)),

    ("RL r",       (0xcb, "00010{0}"),             8, "{0}0 << CY, CY << {0}",               lambda c, r: c.RL_r(r)),
    ("RL (HL)",    (0xcb, 0x16),                  15, "(HL)0 << CY, CY << (HL)",             lambda c:    c.RL_ref_HL()),
    ("RL (ii+d)",  ("11{0}101", 0xcb, "d", 0x16), 23, "({0}+d)0 << CY, CY << ({0}+d)",       lambda c, i: c.RL_ref_index_plus_d(i)),

    ("RRC r",      (0xcb, "00001{0}"),             8, "{0}0 >> {0}7, {0} >> CY",             lambda c, r: c.RRC_r(r)),
    ("RRC (HL)",   (0xcb, 0x0e),                  15, "(HL)0 >> (HL)7, (HL) >> CY",          lambda c:    c.RRC_ref_HL()),
    ("RRC (ii+d)", ("11{0}101", 0xcb, "d", 0x0e), 23, "({0}+d)0 >> ({0}+d)7, ({0}+d) >> CY", lambda c, i: c.RRC_ref_index_plus_d(i)),

    ("RR r",       (0xcb, "00011{0}"),             8, "{0}0 >> CY, {0} >> CY",               lambda c, r: c.RR_r(r)),
    ("RR (HL)",    (0xcb, 0x1e),                  15, "(HL)0 >> CY, (HL) >> CY",             lambda c:    c.RR_ref_HL()),
    ("RR (ii+d)",  ("11{0}101", 0xcb, "d", 0x1e), 23, "({0}+d)0 >> CY, CY >> ({0}+d)",       lambda c, i: c.RR_ref_index_plus_d(i)),

    ("SLA r",      (0xcb, "00100{0}"),             8, "CY << {0}7, {0} << 0",                lambda c, r: c.SLA_r(r)),
    ("SLA (HL)",   (0xcb, 0x26),                  15, "CY << (HL)7, (HL) << 0",              lambda c:    c.SLA_ref_HL()),
    ("SLA (ii+d)", ("11{0}101", 0xcb, "d", 0x26), 23, "CY << ({0}+d)7, ({0}+d) << 0",        lambda c, i: c.SLA_ref_index_plus_d(i)),

    ("SRA r",      (0xcb, "00101{0}"),             8, "{0}7 >> {0}7, {0} >> CY",             lambda c, r: c.SRA_r(r)),
    ("SRA (HL)",   (0xcb, 0x2e),                  15, "(HL)7 >> (HL)7, (HL) >> CY",          lambda c:    c.SRA_ref_HL()),
    ("SRA (ii+d)", ("11{0}101", 0xcb, "d", 0x2e), 23, "({0}+d)7 >> ({0}+d)7, ({0}+d) >> CY", lambda c, i: c.SRA_ref_index_plus_d(i)),

    ("SRL r",      (0xcb, "00111{0}"),             8, "0 >> {0}7, {0} >> CY",                lambda c, r: c.SRL_r(r)),
    ("SRL (HL)",   (0xcb, 0x3e),                  15, "0 >> (HL)7, (HL) >> CY",              lambda c:    c.SRL_ref_HL()),
    ("SRL (ii+d)", ("11{0}101", 0xcb, "d", 0x3e), 23, "0 >> ({0}+d)7, ({0}+d) >> CY",        lambda c, i: c.SRL_ref_index_plus_d(i)),

    ("RLD",        (0xed, 0x6f),                  18, "RLD",                                 lambda c:    c.RLD()),
    ("RRD",        (0xed, 0x67),                  18, "RRD",                                 lambda c:    c.RRD())]

BIT_SET_RESET_TEST_GROUP = [
    ("BIT b, r",      (0xcb, "01{0}{1}"),                   8, "Z <- not({1}{0})",   lambda c, b, r: c.BIT_b_n(b, c.GET_r(r))),
    ("BIT b, (HL)",   (0xcb, "01{0}110"),                  12, "Z <- not((HL){0})",  lambda c, b:    c.BIT_b_n(b, c.GET_ref_HL())),
    ("BIT b, (ii+d)", ("11{1}101", 0xcb, "d", "01{0}110"), 20, "Z <- not(({1} +d))", lambda c, b, i: c.BIT_b_n(b, c.GET_ref_index_plus_d(i))),
    ("SET b, r",      (0xcb, "11{0}{1}"),                   8, "{1}{0} <- 1",        lambda c, b, r: c.SET_b_r(b, r, 1)),
    ("SET b, (HL)",   (0xcb, "11{0}110"),                  15, "(HL){0} <- 1",       lambda c, b:    c.SET_ref_nn(b, c.GET_HL(), 1)),
    ("SET b, (ii+d)", ("11{1}101", 0xcb, "d", "11{0}110"), 23, "({1}+d){0} <- 0",    lambda c, b, i: c.SET_ref_nn(b, c.GET_index_plus_d(i), 1)),
    ("RES b, r",      (0xcb, "10{0}{1}"),                   8, "{1}{0} <- 0",        lambda c, b, r: c.SET_b_r(b, r, 0)),
    ("RES b, (HL)",   (0xcb, "10{0}110"),                  15, "(HL){0} <- 0",       lambda c, b:    c.SET_ref_nn(b, c.GET_HL(), 0)),
    ("RES b, (ii+d)", ("11{1}101", 0xcb, "d", "10{0}110"), 23, "({1}+d){0} <- 0",    lambda c, b, i: c.SET_ref_nn(b, c.GET_index_plus_d(i), 0))]



