Notation Description
--------------------
n 	 Identifies a one-byte unsigned integer expression in the range
         (0 to 255)
nn	 Identifies a two-byte unsigned integer expression in the range
	 (0 to 65535)
d	 Identifies a one-byte signed integer expression in the range
	 (-128 to +127)
e	 Identifies a one-byte signed integer expression in the range
	 (-126 to +129) for relative jump offset from current location
b	 Identifies a one-bit expression in the range (0 to 7).
	 The most-significant bit to the left is bit 7 and the
         least-significant bit to the right is bit 0

(HL)	 Identifies the contents of the memory location,
         whose address is specified by
	 the contents of the register pair HL
(IX+d) 	 Identifies the contents of the memory location,
         whose address is specified by
	 the contents of the Index register pair
         IX plus the signed displacement d
(IY+d)	 Identifies the contents of the memory location,
         whose address is specified by
	 the contents of the Index register pair IY plus
         the signed displacement d

r	 Identifies any of the registers A, B, C, D, E, H, or L
s	 Identifies any of r, n, (HL), (IX+d) or (IY+d)
m	 Identifies any of r, (HL), (IX+d) or (IY+d)

cc	 Identifies the status of the Flag Register as any of
	 (NZ, Z, NC, C, PO, PE, P, or M)
	 for the conditional jumps, calls, and return instructions
qq	 Identifies any of the register pairs BC, DE, HL or AF
dd	 Identifies any of the register pairs BC, DE, HL or SP
pp	 Identifies any of the register pairs BC, DE, IX or SP
rr	 Identifies any of the register pairs BC, DE, IY or SP
ii       Identifies any of the register pairs IX, IY


8 - bit load group
==================
r          bits(t)
B	   000
C	   001
D	   010
E	   011
H	   100
L	   101
A     	   111

ii	   
IX         011
IY         111

Code           | length | opt code
---------------+---------------+--------+----------
LD r, r'       | 1      | 01 r   r'
LD r, n        | 2      | 00 r   110
LD r, (HL)     | 1      | 01 r   110
LD r, (ii + d) | 3      | 11 ii  101  DD/FD
               |        | 01 r   110
	       |        | d
LD (HL), r     | 1      | 01 110 r
LD (HL), n     | 2      | 00 110 110  36
   	       | 	| n
LD (ii + d), r | 3      | 11 ii  101  DD/FD
               |        | 01 110   r
	       |        | d
LD (ii + d), n | 4      | 11 ii  101  DD/FD
               |        | 00 110 110  36
	       |        | d
	       |        | n
LD A, (BC)     | 1      | 00 001 010  0A
LD A, (DE)     | 1      | 00 011 010  1A
LD A, (nn)     | 3      | 00 111 010  3A
               |        | n (low)
	       |        | n (high)
LD (BC), A     | 1      | 00 000 010  02
LD (DE), A     | 1      | 00 010 010  12
LD (nn), A     | 3      | 00 110 010  32
               |        | n
	       |        | n
LD A, I        | 2      | 11 101 101  ED
      	       | 	| 01 010 111  57
LD A, R        | 2      | 11 101 101  ED
               |        | 01 011 111  5F
LD I, A        | 2      | 11 101 101  ED
               |        | 01 000 111  47
LD R, A        | 2      | 11 101 101  ED
               |        | 01 001 111  4F


16 - bit load group
===================

dd |qq |code
---+---+----       
BC |BC | 00
DE |DE | 01
HL |HL | 10
SP |AF | 11
   
Code            | length | opt code
----------------+--------+-----------
LD dd, nn       | 3      | 00 dd 0001
                |        | n
                |        | n
LD IX, nn       | 4      | DD
                |        | 21
                |        | n
                |        | n
LD IY, nn       | 4      | FD
                |        | 21
                |        | n
                |        | n
LD HL, (nn)     | 3      | 2A  | H <- (nn + 1)
                |        | n   | L <- (nn)
                |        | n
LD dd, (nn)     | 4      | ED
                |        | 01 dd 1011
                |        | n
                |        | n
LD IX, (nn)     | 4      | DD
                |        | 2A
                |        | n
                |        | n
LD IY, (nn)     | 4      | FD
                |        | 2A
                |        | n
                |        | n
LD (nn), HL     | 3      | 22 | (nn+1) <- H
                |        | n  | (nn)   <- L
                |        | n
LD (nn), dd     | 4      | ED
                |        | 01 dd 0011 | (nn+1) <- ddh
                |        | n          | (nn) <- ddl
                |        | n
LD (nn), IX     | 4      | DD         | (nn+1) <- IXh
                |        | 22         | (nn)   <- IXl
                |        | n
                |        | n
LD (nn), IY     | 4      | FD         | (nn+1) <- IYh
                |        | 22         | (nn)   <- IXl
                |        | n
                |        | n
LD SP, HL       | 1      | F9         | SP <- HL
LD SP, IX       | 2      | DD         | SP <- IX
                |        | F9         |
LD SP, IY       | 2      | FD         | SP <- IY
                |        | F9
PUSH qq         | 1      | 11 qq 0101 | (SP-1) <- qqh
                |        |            | (SP-2) <- qql
                |        |            | SP <- SP-2
PUSH IX         | 2      | DD         | (SP-1) <- IXh
                |        | E5         | (SP-2) <- IXl
                |        |            | SP <- SP-2
PUSH IY         | 2      | FD         | (SP-2) <- IYh
                |        | E5         | (SP-1) <- IYl
                |        |            | SP <- SP-2
POP qq          | 1      | 11 qq 0001 | qqh <- SP+1
                |        |            | qql <- SP
                |        |            | SP <- SP+2
POP IX          | 2      | DD         | IXh <- SP+1
                |        | E1         | IXl <- SP
                |        |            | SP <- SP+2
POP IY          | 2      | FD         | IYh <- SP+1
                |        | E1         | IYl <- SP
                |        |            | SP <- SP+2
