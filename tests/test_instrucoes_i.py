import pytest
from sim.asm import encode_i
from sim.cpu import execute_i
from sim.registers import RegisterFile

CASOS_I = [
    ("ADDI",       0x0, 7,          5,          12),
    ("ADDI_neg",   0x0, -1,         10,         9),
    ("SLTI",       0x2, 1,          0xFFFFFFFF, 1),
    ("SLTIU",      0x3, 1,          0xFFFFFFFF, 0),
    ("SLTIU_neg",  0x3, -1,         1,          1),
    ("XORI",       0x4, 0b1010,     0b1100,     0b0110),
    ("ORI",        0x6, 0b1010,     0b1100,     0b1110),
    ("ANDI",       0x7, 0b1010,     0b1100,     0b1000),
    ("SLLI",       0x1, 4,          1,          16),
    ("SRLI",       0x5, 4,          0xFFFFFFF0, 0x0FFFFFFF),
    ("SRAI",       0x5, 0x400 | 4,  0xFFFFFFF0, 0xFFFFFFFF),
]

@pytest.mark.parametrize("nome,f3,imm,a,esperado", CASOS_I)
def test_i(nome, f3, imm, a, esperado):
    rf = RegisterFile()
    rf.write(1, a)
    execute_i(rf, encode_i(imm, 1, f3, 3, 0b0010011))
    assert rf.read(3) == esperado, f"{nome}: esperado {esperado:#x}, obtido {rf.read(3):#x}"