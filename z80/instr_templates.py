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
    ("LD A, (nn)",     (0x3a, "n_l", "n_h"),          1, "A <- (nn)",       LD_A_ref_nn),
    ("LD (BC), A",     (0x02),                        1, "(BC) <- A",       LD_ref_BC_A),
    ("LD (DE), A",     (0x12),                        1, "(DE) <- A",       LD_ref_DE_A),
    ("LD (nn), A",     (0x32, "n_l", "n_h"),          1, "(nn) <- A",       LD_ref_nn_A),
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
    ("LD dd, nn",      ("00{0}0001", "n_l", "n_h"),       1, "{0} <- nn",                                    LD_dd_nn),
    ("LD ii, nn",      ("11{0}101", 0x21, "n_l", "n_h"),  1, "{0} <- nn",                                    LD_ii_nn),
    ("LD HL, (nn)",    (0x2a, "n_l", "n_h"),              1, "H <- (nn+1), L <- (nn)",                       LD_HL_ref_nn),
    ("LD dd, (nn)",    (0xed, "01{0}1011", "n_l", "n_h"), 1, "dd_h <- (nn+1), dd_l <- (nn)",                 LD_dd_ref_nn),
    ("LD ii, (nn)",    ("11{0}101", 0x2a, "n_l", "n_h"),  1, "{0}_h <- (nn+1), {0}_l <- (nn)",               LD_ii_ref_nn),
    ("LD (nn), HL",    (0x22, "n_l", "n_h"),              1, "(nn+1) <- H, (nn) <- L",                       LD_ref_nn_HL),
    ("LD (nn), dd",    (0xed, "01{0}0011", "n_l", "n_h"), 1, "(nn+1) <- dd_h, (nn) <- dd_l",                 LD_ref_nn_dd),
    ("LD (nn), ii",    ("11{0}101", 0x22, "n_l", "n_h"),  1, "(nn+1) <- {0}_h, (nn) <- {0}_l",               LD_ref_nn_ii),
    ("LD SP, HL",      (0xf9),                            1, "SP <- HL",                                     LD_SP_HL),
    ("LD SP, ii",      ("11{0}101", 0xf9),                1, "SP <- {0}",                                    LD_SP_ii),
    ("PUSH qq",        ("11{0}0101"),                     1, "(SP-1) <- qq_h, (SP-2) <- qq_l, SP <- SP-2",   PUSH_qq),
    ("PUSH ii",        ("11{0}101", 0xe5),                1, "(SP-1) <- {0}_h, (SP-2) <- {0}_l, SP <- SP-2", PUSH_ii),
    ("POP qq",         ("11{0}0001"),                     1, "qq_h <- (SP+1), qq_l <- (SP), SP <- SP+2",     POP_qq),
    ("POP ii",         ("11{0}101", 0xe1),                1, "{0}_h <- (SP+1), {0}_l <- (SP), SP <- SP+2",   POP_ii)
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
    ("EX (SP), ii", ("11{0}101", 0xe3), 1, "{0}_h <-> (SP+1), {0}_l <-> (SP)",   EX_ref_SP_ii),
]

################################################################################
#
# general purpose group
#
################################################################################
def NOP(cpu):
    pass

GENERAL_PURPOSE = [
    ("NOP", (0x00), 1, "", NOP)
]

