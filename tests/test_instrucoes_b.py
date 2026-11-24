import pytest
from sim.asm import encode_b
from sim.cpu import CPU
from sim.memory import Memory

GRANDE = 0xFFFFFFFF

CASOS_B = [
    ("BEQ_sim",  0x0, 5, 5, True),
    ("BEQ_nao",  0x0, 5, 6, False),
    ("BNE_sim",  0x1, 5, 6, True),
    ("BNE_nao",  0x1, 5, 5, False),
    ("BLT_sim",  0x4, GRANDE, 1, True),   
    ("BLT_nao",  0x4, 1, GRANDE, False),
    ("BGE_sim",  0x5, 1, GRANDE, True),   
    ("BGE_nao",  0x5, GRANDE, 1, False),
    ("BLTU_sim", 0x6, 1, GRANDE, True),   
    ("BLTU_nao", 0x6, GRANDE, 1, False),
    ("BGEU_sim", 0x7, GRANDE, 1, True),
    ("BGEU_nao", 0x7, 1, GRANDE, False),
]

@pytest.mark.parametrize("nome,f3,a,b,salta", CASOS_B)
def test_branch(nome, f3, a, b, salta):
    m = Memory()
    cpu = CPU(m)
    cpu.rf.write(1, a)
    cpu.rf.write(2, b)
    m.write_word(0, encode_b(8, 2, 1, f3, 0b1100011))
    cpu.step()
    assert cpu.pc == (8 if salta else 4), nome