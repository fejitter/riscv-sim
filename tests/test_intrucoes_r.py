import pytest
from sim.asm import encode_r
from sim.cpu import execute_r
from sim.registers import RegisterFile

CASOS_R = [
    ("ADD",  0x0, 0x00, 5, 7, 12),
    ("SUB",  0x0, 0x20, 5, 7, 0xFFFFFFFE),
    ("SLL",  0x1, 0x00, 1, 4, 16),
    ("SLT",  0x2, 0x00, 0xFFFFFFFF, 1, 1),
    ("SLTU", 0x3, 0x00, 0xFFFFFFFF, 1, 0),
    ("XOR",  0x4, 0x00, 0b1100, 0b1010, 0b0110),
    ("SRL",  0x5, 0x00, 0xFFFFFFF0, 4, 0x0FFFFFFF),
    ("SRA",  0x5, 0x20, 0xFFFFFFF0, 4, 0xFFFFFFFF),
    ("OR",   0x6, 0x00, 0b1100, 0b1010, 0b1110),
    ("AND",  0x7, 0x00, 0b1100, 0b1010, 0b1000),
]

@pytest.mark.parametrize("nome,f3,f7,a,b,esperado", CASOS_R)
def test_r(nome, f3, f7, a, b, esperado):
    rf = RegisterFile()
    rf.write(1, a)
    rf.write(2, b)
    execute_r(rf, encode_r(f7, 2, 1, f3, 3, 0b0110011))
    assert rf.read(3) == esperado, f"{nome}: esperado {esperado:#x}, obtido {rf.read(3):#x}"