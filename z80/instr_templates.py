# flake8: noqa
################################################################################
#
# 8 bit load group
#
################################################################################
def LD_r_r(cpu, rd, rs):
    cpu.LD_r_n(rd, cpu.GET_r(rs))

def LD_r_n(cpu, r):
    cpu.LD_r_n(r, cpu.GET_ref_PC_plus_d(1))

def LD_r_ref_HL(cpu, r):
    cpu.LD_r_n(r, cpu.GET_ref_nn(cpu.GET_HL()))

def LD_r_ref_index_plus_d(cpu, r, ii):
    d = n2d(cpu.GET_ref_PC_plus_d(2))
    cpu.LD_r_n(r, cpu.GET_ref_nn(cpu.GET_ii_plus_d(ii, d)))

def LD_ref_HL_r(cpu, r):
    cpu.LD_ref_nn_n(cpu.GET_HL(), cpu.GET_r(r))

def LD_ref_HL_n(cpu):
    cpu.LD_ref_nn_n(cpu.GET_HL(), cpu.GET_ref_PC_plus_d(1))

def LD_ref_index_plus_d_r(cpu, ii, r):
    d = n2d(cpu.GET_ref_PC_plus_d(2))
    cpu.LD_ref_nn_n(cpu.GET_ii_plus_d(ii, d),
                    cpu.GET_r(r))

def LD_ref_index_plus_d_n(cpu, ii):
    d = n2d(cpu.GET_ref_PC_plus_d(2))
    n = cpu.GET_ref_PC_plus_d(3)
    cpu.LD_ref_nn_n(cpu.GET_ii_plus_d(ii, d), n)

def LD_A_ref_BC(cpu):
    cpu.LD_A_n(cpu.GET_ref_nn(cpu.GET_BC()))

def LD_A_ref_DE(cpu):
    cpu.LD_A_n(c.GET_ref_nn(cpu.GET_DE()))

def LD_A_ref_nn(cpu):
    nn = (cpu.GET_PC_plus_d(2) << 8) + cpu.GET_PC_plus_d(1)
    cpu.LD_A_n(cpu.GET_ref_nn(nn))

def LD_ref_BC_A(cpu):
    cpu.LD_ref_nn_n(cpu.GET_BC(), cpu.GET_A())

def LD_ref_DE_A(cpu):
    cpu.LD_ref_nn_n(cpu.GET_DE(), cpu.GET_A())

def LD_ref_nn_A(cpu):
    nn = (cpu.GET_PC_plus_d(2) << 8) + cpu.GET_PC_plus_d(1)
    cpu.LD_ref_nn_n(nn, cpu.GET_A())

def LD_A_I(cpu):
    cpu.LD_A_n(cpu.GET_I())

def LD_A_R(cpu):
    cpu.LD_A_n(cpu.GET_R())

def LD_I_A(cpu):
    cpu.LD_I_n(cpu.GET_A())

def LD_R_A(cpu):
    cpu.LD_R_n(cpu.GET_A())


EIGHT_BIT_LOAD_GROUP = [
    ("LD r, r",        ("01{0}{1}"),                  1, "{0} <- {1}",      LD_r_r),
    ("LD r, n",        ("00{0}110", "n"),             1, "{0} <- n",        LD_r_n),
    ("LD r, (HL)",     ("01{0}110"),                  1, "{0} <- (HL)",     LD_r_ref_HL),
    ("LD r, (ii + d)", ("11{1}101", "01{0}110", "d"), 1, "{0} <- ({1}+d)",  LD_r_ref_index_plus_d),
    ("LD (HL), r",     ("01110{0}"),                  1, "(HL) <- {0}",     LD_ref_HL_r),
    ("LD (HL), n",     (0x36, "n"),                   1, "(HL) <- n",       LD_ref_HL_n),
    ("LD (ii + d), r", ("11{0}101", "01110{1}", "d"), 1, "({0}+d) <- {1}",  LD_ref_index_plus_d_r),
    ("LD (ii + d), n", ("11{0}101", 0x36, "d", "n"),  1, "({0}+d) <- n",    LD_ref_index_plus_d_n),
    ("LD A, (BC)",     (0x0a),                        1, "A <- (BC)",       LD_A_ref_BC),
    ("LD A, (DE)",     (0x1a),                        1, "A <- (DE)",       LD_A_ref_DE),
    ("LD A, (nn)",     (0x3a, "nl", "nh"),            1, "A <- (nn)",       LD_A_ref_nn),
    ("LD (BC), A",     (0x02),                        1, "(BC) <- A",       LD_ref_BC_A),
    ("LD (DE), A",     (0x12),                        1, "(DE) <- A",       LD_ref_DE_A),
    ("LD (nn), A",     (0x32, "nl", "nh"),            1, "(nn) <- A",       LD_ref_nn_A),
    ("LD A, I",        (0xed, 0x57),                  1, "A <- I",          LD_A_I),
    ("LD A, R",        (0xed, 0x5f),                  1, "A <- R",          LD_A_R),
    ("LD I, A",        (0xed, 0x47),                  1, "I <- A",          LD_I_A),
    ("LD R, A",        (0xed, 0x4f),                  1, "R <- A",          LD_R_A)]

################################################################################
#
# 16 bit load group
#
################################################################################
def LD_dd_nn(cpu, dd):
    cpu.LD_dd_nn(dd, cpu.GET_ref2_PC_plus_d(1))

def LD_ii_nn(cpu, ii):
    cpu.LD_index_nn(ii, cpu.GET_ref2_PC_plus_d(2))

def LD_HL_ref_nn(cpu):
    cpu.LD_dd_nn('HL', cpu.GET_ref2_PC_plus_d(1))

def LD_dd_ref_nn(cpu):
    cpu.LD_dd_nn(dd, cpu.GET_ref2_PC_plus_d(2))

def LD_ii_ref_nn(cpu):
    cpu.LD_ii_nn(ii, cpu.GET_ref2_PC_plus_d(2))

def LD_ref_nn_HL(cpu):
    cpu.LD_ref_nn_nn(cpu.GET_ref2_PC_plus_d(1), cpu.GET_HL())

def LD_ref_nn_dd(cpu, dd):
    cpu.LD_ref_nn_nn(cpu.GET_ref2_PC_plus_d(2), cpu.GET_ii(dd))

def LD_ref_nn_ii(cpu, ii):
    cpu.LD_ref_nn_nn(cpu.GET_ref2_PC_plus_d(2), cpu.GET_ii(ii))

def LD_SP_HL(cpu):
    cpu.LD_SP_nn(cpu.GET_HL())

def LD_SP_ii(cpu):
    cpu.LD_SP_nn(cpu.GET_ii(ii))

def PUSH_qq(cpu, qq):
    cpu.DEC_SP(2)
    cpu.LD_ref_nn_nn(cpu.GET_SP(), cpu.GET_ii(qq))

def PUSH_ii(cpu, ii):
    cpu.DEC_SP(2)
    cpu.LD_ref_nn_nn(cpu.GET_SP(), cpu.GET_ii(ii))

def POP_qq(cpu ,qq):
    cpu.LD_ii_nn(qq, cpu.GET_ref_nn(cpu.GET_SP()))
    cpu.INC_SP(2)

def POP_ii(cpu, ii):
    cpu.LD_ii_nn(ii, cpu.GET_ref_nn(cpu.GET_SP()))
    cpu.INC_SP(2)

SIXTEEN_BIT_LOAD_GROUP = [
    ("LD dd, nn",      ("00{0}0001", "nl", "nh"),       1, "{0} <- nn",                                    LD_dd_nn),
    ("LD ii, nn",      ("11{0}101", 0x21, "nl", "nh"),  1, "{0} <- nn",                                    LD_ii_nn),
    ("LD HL, (nn)",    (0x2a, "nl", "nh"),              1, "H <- (nn+1), L <- (nn)",                       LD_HL_ref_nn),
    ("LD dd, (nn)",    (0xed, "01{0}1011", "nl", "nh"), 1, "dd_h <- (nn+1), dd_l <- (nn)",                 LD_dd_ref_nn),
    ("LD ii, (nn)",    ("11{0}101", 0x2a, "nl", "nh"),  1, "{0}_h <- (nn+1), {0}_l <- (nn)",               LD_ii_ref_nn),
    ("LD (nn), HL",    (0x22, "nl", "nh"),              1, "(nn+1) <- H, (nn) <- L",                       LD_ref_nn_HL),
    ("LD (nn), dd",    (0xed, "01{0}0011", "nl", "nh"), 1, "(nn+1) <- dd_h, (nn) <- dd_l",                 LD_ref_nn_dd),
    ("LD (nn), ii",    ("11{0}101", 0x22, "nl", "nh"),  1, "(nn+1) <- {0}_h, (nn) <- {0}_l",               LD_ref_nn_ii),
    ("LD SP, HL",      (0xf9),                          1, "SP <- HL",                                     LD_SP_HL),
    ("LD SP, ii",      ("11{0}101", 0xf9),              1, "SP <- {0}",                                    LD_SP_ii),
    ("PUSH qq",        ("11{0}0101"),                   1, "(SP-1) <- qq_h, (SP-2) <- qq_l, SP <- SP-2",   PUSH_qq),
    ("PUSH ii",        ("11{0}101", 0xe5),              1, "(SP-1) <- {0}_h, (SP-2) <- {0}_l, SP <- SP-2", PUSH_ii),
    ("POP qq",         ("11{0}0001"),                   1, "qq_h <- (SP+1), qq_l <- (SP), SP <- SP+2",     POP_qq),
    ("POP ii",         ("11{0}101", 0xe1),              1, "{0}_h <- (SP+1), {0}_l <- (SP), SP <- SP+2",   POP_ii)
]

################################################################################
#
# exchange group
#
################################################################################
def EX_DE_HL(cpu):
    tmp = cpu.GET_DE()
    cpu.LD_ii_nn('DE', cpu.GET_HL())
    cpu.LD_ii_nn('HL', tmp)

def EX_AF_altAF(cpu):
    cpu.EX_q_altq('A')
    cpu.EX_q_altq('F')

def EXX(cpu):
    cpu.EX_q_altq('B')
    cpu.EX_q_altq('C')
    cpu.EX_q_altq('D')
    cpu.EX_q_altq('E')
    cpu.EX_q_altq('H')
    cpu.EX_q_altq('L')

def EX_ref_SP_HL(cpu):
    tmp = cpu.GET_ref2_nn(cpu.SP())
    cpu.LD_ref2_nn_nn(cpu.SP(), cpu.GET_HL())
    cpu.LD_ii('HL', tmp)

def EX_ref_SP_ii(cpu, ii):
    tmp = cpu.GET_ref2_nn(cpu.SP())
    cpu.LD_ref2_nn_nn(cpu.SP(), cpu.GET_ii(ii))
    cpu.LD_ii(ii, tmp)

EXCHANGE_GROUP = [
    ("EX DE, HL",   (0xeb),             1, "DE <-> HL",                          EX_DE_HL),
    ("EX AF, AF'",  (0x08),             1, "AF <-> AF'",                         EX_AF_altAF),
    ("EXX",         (0xd9),             1, "BC <-> BC', DE <-> DE', HL <-> HL'", EXX),
    ("EX (SP), HL", (0xe3),             1, "H <-> (SP+1), L <-> (SP)",           EX_ref_SP_HL),
    ("EX (SP), ii", ("11{0}101", 0xe3), 1, "{0}_h <-> (SP+1), {0}_l <-> (SP)",   EX_ref_SP_ii)]

################################################################################
#
# block transfer group
#
################################################################################
def LDI(cpu):
    cpu.LD_ref_nn_n(cpu.GET_DE(), cpu.GET_ref_nn(cpu.GET_HL()))
    cpu.INC_ii('DE')
    cpu.INC_ii('HL')
    cpu.DEC_ii('BC')
    cpu.UNSET_FLAG('H')
    cpu.UNSET_FLAG('N')
    if cpu.GET_BC() == 1:
        cpu.SET_FLAG('V')
    else:
        cpu.UNSET_FLAG('V')

def LDIR(cpu):
    LDI(cpu)
    if cpu.GET_BC() != 0x0000:
        cpu.DEC_PC(2)

def LDD(cpu):
    cpu.LD_ref_nn_n(cpu.GET_DE(), cpu.GET_ref_nn(cpu.GET_HL()))
    cpu.DEC_ii('DE')
    cpu.DEC_ii('HL')
    cpu.DEC_ii('BC')
    cpu.UNSET_FLAG('H')
    cpu.UNSET_FLAG('N')
    if cpu.GET_BC() == 1:
        cpu.SET_FLAG('V')
    else:
        cpu.UNSET_FLAG('V')


def LDDR(cpu):
    LDD(cpu)
    if cpu.GET_BC() != 0x0000:
        cpu.DEC_PC(2)

# todo: make t-states dynamic, depending on the result
# T-states for LDIR and LDDR: if BC = 0: 16
BLOCK_TRANSFER_GROUP = [
    ("LDI",  (0xed, 0xa0), 16, "(DE) <- (HL), DE <- DE + 1, HL <- HL + 1, BC <- BC - 1",               LDI),
    ("LDIR", (0xed, 0xb0), 21, "(DE) <- (HL), DE <- DE + 1, HL <- HL + 1, BC <- BC - 1 WHILE BC != 0", LDIR),
    ("LDD",  (0xed, 0xa8), 16, "(DE) <- (HL), DE <- DE - 1, HL <- HL - 1, BC <- BC - 1",               LDD),
    ("LDDR", (0xed, 0xb8), 21, "(DE) <- (HL), DE <- DE - 1, HL <- HL - 1, BC <- BC - 1 WHILE BC != 0", LDDR)]

################################################################################
#
# Search group
#
################################################################################
# todo: make t-states dynamic, depending on the result
# T-states for CPIR and CPDR: if BC = 0 and A=(HL): 16
def CPI(cpu):
    cpu.CP_A_n(cpu.GET_ref_nn(cpu.GET_HL()), False)
    cpu.SET_FLAG('V', cpu.GET_BC() != 0x00001)
    cpu.INC_ii('HL')
    cpu.DEC_ii('BC')

def CPIR(cpu):
    CPI(cpu)
    if cpu.GET_BC() != 0x0000:
        cpu.DEC_PC(2)    

def CPD(cpu):
    cpu.CP_A_n(cpu.GET_ref_nn(cpu.GET_HL()), False)
    cpu.SET_FLAG('V', cpu.GET_BC() != 0x00001)
    cpu.DEC_ii('HL')
    cpu.DEC_ii('BC')

def CPDR(cpu):
    CPD(cpu)
    if cpu.GET_BC() != 0x0000:
        cpu.DEC_PC(2)    

SEARCH_GROUP = [
    ("CPI",  (0xed, 0xa1), 16, "A - (HL), HL <- HL + 1, BC <- BC - 1", CPI),
    ("CPIR", (0xed, 0xb1), 21, "A - (HL), HL <- HL + 1, BC <- BC - 1", CPIR),
    ("CPD",  (0xed, 0xa9), 16, "A - (HL), HL <- HL - 1, BC <- BC - 1", CPD),
    ("CPDR", (0xed, 0xb9), 16, "A - (HL), HL <- HL - 1, BC <- BC - 1", CPDR)]

################################################################################
#
# 8-bit arithmetic group
#
################################################################################
def ADD_A_r(cpu, r):
    cpu.ADD_A_n(cpu.GET_r(r))

def ADD_A_n(cpu):
    cpu.ADD_A_n(cpu.GET_ref_PC_plus_d(1))

def ADD_A_ref_HL(cpu):
    cpu.ADD_A_n(cpu.GET_ref_nn(cpu.GET_HL()))

def ADD_A_ref_index_plus_d(cpu, ii):
    d = n2d(cpu.GET_ref_PC_plus_d(2))
    cpu.ADD_A_n(cpu.GET_ref_nn(cpu.GET_ii_plus_d(ii, d)))

def ADC_A_r(cpu, r):
    cpu.ADD_A_n(cpu.GET_r(r), cpu.GET_FLAG('C'))

def ADC_A_n(cpu):
    cpu.ADD_A_n(cpu.GET_ref_PC_plus_d(1), cpu.GET_FLAG('C'))

def ADC_A_ref_HL(cpu):
    cpu.ADD_A_n(cpu.GET_ref_nn(cpu.GET_HL()), cpu.GET_FLAG('C'))

def ADC_A_ref_index_plus_d(cpu, ii):
    d = n2d(cpu.GET_ref_PC_plus_d(2))
    cpu.ADD_A_n(cpu.GET_ref_nn(cpu.GET_ii_plus_d(ii, d)), cpu.GET_FLAG('C'))

def SUB_A_r(cpu, r):
    cpu.SUB_A_n(cpu.GET_r(r))

def SUB_A_n(cpu):
    cpu.SUB_A_n(cpu.GET_ref_PC_plus_d(1))

def SUB_A_ref_HL(cpu):
    cpu.SUB_A_n(cpu.GET_ref_nn(cpu.GET_HL()))

def SUB_A_ref_index_plus_d(cpu, ii):
    d = n2d(cpu.GET_ref_PC_plus_d(2))
    cpu.SUB_A_n(cpu.GET_ref_nn(cpu.GET_ii_plus_d(ii, d)))

def SBC_A_r(cpu, r):
    cpu.SUB_A_n(cpu.GET_r(r), cpu.GET_FLAG('C'))

def SBC_A_n(cpu):
    cpu.SUB_A_n(cpu.GET_ref_PC_plus_d(1), cpu.GET_FLAG('C'))

def SBC_A_ref_HL(cpu):
    cpu.SUB_A_n(cpu.GET_ref_nn(cpu.GET_HL()), cpu.GET_FLAG('C'))

def SBC_A_ref_index_plus_d(cpu, ii):
    d = n2d(cpu.GET_ref_PC_plus_d(2))
    cpu.SUB_A_n(cpu.GET_ref_nn(cpu.GET_ii_plus_d(ii, d)), cpu.GET_FLAG('C'))

def AND_A_r(cpu, r):
    cpu.AND_A_n(cpu.GET_r(r))

def AND_A_n(cpu):
    cpu.AND_A_n(cpu.GET_ref_PC_plus_d(1))

def AND_A_ref_HL(cpu):
    cpu.AND_A_n(cpu.GET_ref_nn(cpu.GET_HL()))

def AND_A_ref_index_plus_d(cpu, ii):
    d = n2d(cpu.GET_ref_PC_plus_d(2))
    cpu.AND_A_n(cpu.GET_ref_nn(cpu.GET_ii_plus_d(ii, d)))

def OR_A_r(cpu, r):
    cpu.OR_A_n(cpu.GET_r(r))

def OR_A_n(cpu):
    cpu.OR_A_n(cpu.GET_ref_PC_plus_d(1))

def OR_A_ref_HL(cpu):
    cpu.OR_A_n(cpu.GET_ref_nn(cpu.GET_HL()))

def OR_A_ref_index_plus_d(cpu, ii):
    d = n2d(cpu.GET_ref_PC_plus_d(2))
    cpu.OR_A_n(cpu.GET_ref_nn(cpu.GET_ii_plus_d(ii, d)))

def XOR_A_r(cpu, r):
    cpu.XOR_A_n(cpu.GET_r(r))

def XOR_A_n(cpu):
    cpu.XOR_A_n(cpu.GET_ref_PC_plus_d(1))

def XOR_A_ref_HL(cpu):
    cpu.XOR_A_n(cpu.GET_ref_nn(cpu.GET_HL()))

def XOR_A_ref_index_plus_d(cpu, ii):
    d = n2d(cpu.GET_ref_PC_plus_d(2))
    cpu.XOR_A_n(cpu.GET_ref_nn(cpu.GET_ii_plus_d(ii, d)))

def CP_A_r(cpu, r):
    cpu.CP_A_n(cpu.GET_r(r))

def CP_A_n(cpu):
    cpu.CP_A_n(cpu.GET_ref_PC_plus_d(1))

def CP_A_ref_HL(cpu):
    cpu.CP_A_n(cpu.GET_ref_nn(cpu.GET_HL()))

def CP_A_ref_index_plus_d(cpu, ii):
    d = n2d(cpu.GET_ref_PC_plus_d(2))
    cpu.CP_A_n(cpu.GET_ref_nn(cpu.GET_ii_plus_d(ii, d)))

def INC_r(cpu, r):
    cpu.LD_r_n(r, cpu.INC_n(cpu.GET_r(r)))

def INC_ref_HL(cpu):
    cpu.LD_ref_HL_n(cpu.INC_n(cpu.GET_ref_nn(cpu.GET_HL())))

def INC_ref_index_plus_d(cpu):
    d = n2d(cpu.GET_ref_PC_plus_d(2))
    nn = cpu.GET_ii_plus_d(ii, d)
    cpu.LD_ref_nn_n(nn, cpu.INC_n(cpu.GET_ref_nn(nn)))

def DEC_r(cpu):
    cpu.LD_r_n(r, cpu.DEC_n(cpu.GET_r(r)))

def DEC_ref_HL(cpu):
    cpu.LD_ref_HL_n(cpu.DEC_n(cpu.GET_ref_nn(cpu.GET_HL())))

def DEC_ref_index_plus_d(cpu):
    d = n2d(cpu.GET_ref_PC_plus_d(2))
    nn = cpu.GET_ii_plus_d(ii, d)
    cpu.LD_ref_nn_n(nn, cpu.DEC_n(cpu.GET_ref_nn(nn)))


EIGHT_BIT_ARITHMETIC_GROUP = [
    ("ADD A, r",        ("10000{0}"),             4,  "A <- A + {0}",               ADD_A_r),
    ("ADD A, n",        (0xc6, "n"),              7,  "A <- A + n",                 ADD_A_n),
    ("ADD A, (HL)",     (0x86),                   7,  "A <- A + (HL)",              ADD_A_ref_HL),
    ("ADD A, (ii + d)", ("11{0}101", 0x86, "d"),  19, "A <- A + ({0}+d)",           ADD_A_ref_index_plus_d),

    ("ADC A, r",        ("10001{0}"),             4,  "A <- A + {0} + CY",          ADC_A_r),
    ("ADC A, n",        (0xce, "n"),              7,  "A <- A + n",                 ADC_A_n),
    ("ADC A, (HL)",     (0x8e),                   7,  "A <- A + (HL)",              ADC_A_ref_HL),
    ("ADC A, (ii + d)", ("11{0}101", 0x8e, "d"),  19, "A <- A + ({0}+d)",           ADC_A_ref_index_plus_d),

    ("SUB A, r",        ("10010{0}"),             4,  "A <- A - {0}",               SUB_A_r),
    ("SUB A, n",        (0xd6, "n"),              7,  "A <- A - n",                 SUB_A_n),
    ("SUB A, (HL)",     (0x96),                   7,  "A <- A - (HL)",              SUB_A_ref_HL),
    ("SUB A, (ii + d)", ("11{0}101", 0x96, "d"),  19, "A <- A - ({0}+d)",           SUB_A_ref_index_plus_d),

    ("SBC A, r",        ("10011{0}"),             4,  "A <- A - {0} - CY",          SBC_A_r),
    ("SBC A, n",        (0xde, "n"),              7,  "A <- A - n - CY",            SBC_A_n),
    ("SBC A, (HL)",     (0x9e),                   7,  "A <- A - (HL) - CY",         SBC_A_ref_HL),
    ("SBC A, (ii + d)", ("11{0}101", 0x9e, "d"),  19, "A <- A - ({0}+d)",           SBC_A_ref_index_plus_d),

    ("AND A, r",        ("10100{0}"),             4,  "A <- A AND {0}",             AND_A_r),
    ("AND A, n",        (0xe6, "n"),              7,  "A <- A AND n",               AND_A_n),
    ("AND A, (HL)",     (0xa6),                   7,  "A <- A AND (HL)",            AND_A_ref_HL),
    ("AND A, (ii + d)", ("11{0}101", 0xa6, "d"),  19, "A <- A AND ({0}+d)",         AND_A_ref_index_plus_d),

    ("OR A, r",         ("10110{0}"),             4,  "A <- A OR {0}",              OR_A_r),
    ("OR A, n",         (0xf6, "n"),              7,  "A <- A OR n",                OR_A_n),
    ("OR A, (HL)",      (0xb6),                   7,  "A <- A OR (HL)",             OR_A_ref_HL),
    ("OR A, (ii + d)",  ("11{0}101", 0xb6, "d"),  19, "A <- A OR ({0}+d)",          OR_A_ref_index_plus_d),

    ("XOR A, r",        ("10101{0}"),             4,  "A <- A XOR {0}",             XOR_A_r),
    ("XOR A, n",        (0xee, "n"),              7,  "A <- A XOR n",               XOR_A_n),
    ("XOR A, (HL)",     (0xae),                   7,  "A <- A XOR (HL)",            XOR_A_ref_HL),
    ("XOR A, (ii + d)", ("11{0}101", 0xae, "d"),  19, "A <- A XOR ({0}+d)",         XOR_A_ref_index_plus_d),

    ("CP r",            ("10111{0}"),             4,  "A - {0}",                    CP_A_r),
    ("CP n",            (0xfe, "n"),              7,  "A - n",                      CP_A_n),
    ("CP (HL)",         (0xbe),                   7,  "A - (HL)",                   CP_A_ref_HL),
    ("CP (ii + d)",     ("11{0}101", 0xbe, "d"),  19, "A - ({0}+d)",                CP_A_ref_index_plus_d),

    ("INC r",           ("00{0}100"),             4,  "{0} <- {0} + 1",             INC_r),
    ("INC (HL)",        (0x34),                   11, "(HL) < (HL) + 1",            INC_ref_HL),
    ("INC (ii + d)",    ("11{0}101", 0x34, "d"),  23, "({0} + d) <- ({0} + d) + 1", INC_ref_index_plus_d),

    ("DEC r",           ("00{0}101"),             4,  "{0} <- {0} + 1",             DEC_r),
    ("DEC (HL)",        (0x35),                   11, "(HL) < (HL) + 1",            DEC_ref_HL),
    ("DEC (ii + d)",    ("11{0}101", 0x35, "d"),  23, "({0} + d) <- ({0} + d) + 1", DEC_ref_index_plus_d)]

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
    ("INC ss",     ("00{0}0011"),        6, "{0} <- {0} + 1",      INC_ss),
    ("INC ii",     ("11{0}101", 0x23),  10, "{0} <- {0} + 1",      INC_ii),
    ("DEC ss",     ("00{0}1011"),        6, "{0} <- {0} - 1",      DEC_ss),
    ("DEC ii",     ("11{0}101", 0x2b),  10, "{0} <- {0} - 1",      DEC_ii)]

################################################################################
#
# rotate and shift group
#
################################################################################
## RLC ##
def RLC_r(cpu, r):
    cpu.LD_r_n(r, cpu.shift_left_n(cpu.GET_r(r), 'RLC'))

def RLC_ref_HL(cpu):
    nn = cpu.GET_HL()
    cpu.LD_ref_nn_n(nn, cpu.shift_left_n(cpu.GET_ref_nn(nn), 'RLC'))

def RLC_ref_index_plus_d(cpu, ii):
    d = n2d(cpu.GET_ref_PC_plus_d(2))
    nn = cpu.GET_ii_plus_d(ii, d)
    cpu.LD_ref_nn_n(nn, cpu.shift_left_n(cpu.GET_ref_nn(nn), 'RLC'))

## RL ##
def RL_r(cpu, r):
    cpu.LD_r_n(r, cpu.shift_left_n(cpu.GET_r(r), 'RL'))

def RL_ref_HL(cpu):
    nn = cpu.GET_HL()
    cpu.LD_ref_nn_n(nn, cpu.shift_left_n(cpu.GET_ref_nn(nn), 'RL'))

def RL_ref_index_plus_d(cpu, ii):
    d = n2d(cpu.GET_ref_PC_plus_d(2))
    nn = cpu.GET_ii_plus_d(ii, d)
    cpu.LD_ref_nn_n(nn, cpu.shift_left_n(cpu.GET_ref_nn(nn), 'RL'))

## SLA ##
def SLA_r(cpu, r):
    cpu.LD_r_n(r, cpu.shift_left_n(cpu.GET_r(r), 'SLA'))

def SLA_ref_HL(cpu):
    nn = cpu.GET_HL()
    cpu.LD_ref_nn_n(nn, cpu.shift_left_n(cpu.GET_ref_nn(nn), 'SLA'))

def SLA_ref_index_plus_d(cpu, ii):
    d = n2d(cpu.GET_ref_PC_plus_d(2))
    nn = cpu.GET_ii_plus_d(ii, d)
    cpu.LD_ref_nn_n(nn, cpu.shift_left_n(cpu.GET_ref_nn(nn), 'SLA'))

## RRC ##
def RRC_r(cpu, r):
    cpu.LD_r_n(r, cpu.shift_right_n(cpu.GET_r(r), 'RRC'))

def RRC_ref_HL(cpu):
    nn = cpu.GET_HL()
    cpu.LD_ref_nn_n(nn, cpu.shift_right_n(cpu.GET_ref_nn(nn), 'RRC'))

def RRC_ref_index_plus_d(cpu, ii):
    d = n2d(cpu.GET_ref_PC_plus_d(2))
    nn = cpu.GET_ii_plus_d(ii, d)
    cpu.LD_ref_nn_n(nn, cpu.shift_right_n(cpu.GET_ref_nn(nn), 'RRC'))

## RR ##
def RR_r(cpu, r):
    cpu.LD_r_n(r, cpu.shift_right_n(cpu.GET_r(r), 'RR'))

def RR_ref_HL(cpu):
    nn = cpu.GET_HL()
    cpu.LD_ref_nn_n(nn, cpu.shift_right_n(cpu.GET_ref_nn(nn), 'RR'))

def RR_ref_index_plus_d(cpu, ii):
    d = n2d(cpu.GET_ref_PC_plus_d(2))
    nn = cpu.GET_ii_plus_d(ii, d)
    cpu.LD_ref_nn_n(nn, cpu.shift_right_n(cpu.GET_ref_nn(nn), 'RR'))

## SRA ##
def SRA_r(cpu, r):
    cpu.LD_r_n(r, cpu.shift_right_n(cpu.GET_r(r), 'SRA'))

def SRA_ref_HL(cpu):
    nn = cpu.GET_HL()
    cpu.LD_ref_nn_n(nn, cpu.shift_right_n(cpu.GET_ref_nn(nn), 'SRA'))

def SRA_ref_index_plus_d(cpu, ii):
    d = n2d(cpu.GET_ref_PC_plus_d(2))
    nn = cpu.GET_ii_plus_d(ii, d)
    cpu.LD_ref_nn_n(nn, cpu.shift_right_n(cpu.GET_ref_nn(nn), 'SRA'))

## SRL ##
def SRL_r(cpu, r):
    cpu.LD_r_n(r, cpu.shift_right_n(cpu.GET_r(r), 'SRL'))

def SRL_ref_HL(cpu):
    nn = cpu.GET_HL()
    cpu.LD_ref_nn_n(nn, cpu.shift_right_n(cpu.GET_ref_nn(nn), 'SRL'))

def SRL_ref_index_plus_d(cpu, ii):
    d = n2d(cpu.GET_ref_PC_plus_d(2))
    nn = cpu.GET_ii_plus_d(ii, d)
    cpu.LD_ref_nn_n(nn, cpu.shift_right_n(cpu.GET_ref_nn(nn), 'SRL'))

## RLD RRD ##
def RLD(cpu):
    nn = cpu.GET_HL()
    cpu.LD_ref_nn_n(nn, cpu.RLD_n(cpu.GET_ref_nn(nn)))

def RRD(cpu):
    nn = cpu.GET_HL()
    cpu.LD_ref_nn_n(nn, cpu.RRD_n(cpu.GET_ref_nn(nn)))


ROTATE_AND_SHIFT_GROUP = [
    ("RLCA",       (0x07),                         4, "A0 << A7, CY << A",                   lambda cpu: RLC_r(cpu, 'A')),
    ("RLA",        (0x17),                         4, "A0 << CY, CY << A",                   lambda cpu: RL_r(cpu, 'A')),
    ("RRCA",       (0x0f),                         4, "A0 >> A7, A >> CY",                   lambda cpu: RRC_r(cpu, 'A')),
    ("RRA",        (0x1f),                         4, "CY >> A7, A >> CY",                   lambda cpu: RR_r(cpu, 'A')),

    ("RLC r",      (0xcb, "00000{0}"),             8, "{0}0 << {0}7, CY << {0}",             RLC_r),
    ("RLC (HL)",   (0xcb, 0x06),                  15, "(HL)0 << (HL)7, CY << (HL)",          RLC_ref_HL),
    ("RLC (ii+d)", ("11{0}101", 0xcb, "d", 0x06), 23, "({0}+d)0 << ({0}+d)7, CY << ({0}+d)", RLC_ref_index_plus_d),

    ("RL r",       (0xcb, "00010{0}"),             8, "{0}0 << CY, CY << {0}",               RL_r),
    ("RL (HL)",    (0xcb, 0x16),                  15, "(HL)0 << CY, CY << (HL)",             RL_ref_HL),
    ("RL (ii+d)",  ("11{0}101", 0xcb, "d", 0x16), 23, "({0}+d)0 << CY, CY << ({0}+d)",       RL_ref_index_plus_d),

    ("RRC r",      (0xcb, "00001{0}"),             8, "{0}0 >> {0}7, {0} >> CY",             RRC_r),
    ("RRC (HL)",   (0xcb, 0x0e),                  15, "(HL)0 >> (HL)7, (HL) >> CY",          RRC_ref_HL),
    ("RRC (ii+d)", ("11{0}101", 0xcb, "d", 0x0e), 23, "({0}+d)0 >> ({0}+d)7, ({0}+d) >> CY", RRC_ref_index_plus_d),

    ("RR r",       (0xcb, "00011{0}"),             8, "{0}0 >> CY, {0} >> CY",               RR_r),
    ("RR (HL)",    (0xcb, 0x1e),                  15, "(HL)0 >> CY, (HL) >> CY",             RR_ref_HL),
    ("RR (ii+d)",  ("11{0}101", 0xcb, "d", 0x1e), 23, "({0}+d)0 >> CY, CY >> ({0}+d)",       RR_ref_index_plus_d),

    ("SLA r",      (0xcb, "00100{0}"),             8, "CY << {0}7, {0} << 0",                SLA_r),
    ("SLA (HL)",   (0xcb, 0x26),                  15, "CY << (HL)7, (HL) << 0",              SLA_ref_HL),
    ("SLA (ii+d)", ("11{0}101", 0xcb, "d", 0x26), 23, "CY << ({0}+d)7, ({0}+d) << 0",        SLA_ref_index_plus_d),

    ("SRA r",      (0xcb, "00101{0}"),             8, "{0}7 >> {0}7, {0} >> CY",             SRA_r),
    ("SRA (HL)",   (0xcb, 0x2e),                  15, "(HL)7 >> (HL)7, (HL) >> CY",          SRA_ref_HL),
    ("SRA (ii+d)", ("11{0}101", 0xcb, "d", 0x2e), 23, "({0}+d)7 >> ({0}+d)7, ({0}+d) >> CY", SRA_ref_index_plus_d),

    ("SRL r",      (0xcb, "00111{0}"),             8, "0 >> {0}7, {0} >> CY",                SRL_r),
    ("SRL (HL)",   (0xcb, 0x3e),                  15, "0 >> (HL)7, (HL) >> CY",              SRL_ref_HL),
    ("SRL (ii+d)", ("11{0}101", 0xcb, "d", 0x3e), 23, "0 >> ({0}+d)7, ({0}+d) >> CY",        SRL_ref_index_plus_d),

    ("RLD",        (0xed, 0x6f),                  18, "RLD",                                 RLD),
    ("RRD",        (0xed, 0x67),                  18, "RRD",                                 RRD)]


