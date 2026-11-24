import pytest
from sim.machine import Machine

def test_perifericos_mapeados():
    m = Machine()
    m.bus.write_word(0x9FC00, 0x41)
    assert m.per.read_word(0) == 0x41
    assert m.bus.read_word(0x9FC00) == 0x41

def test_ultima_palavra_dos_perifericos():
    m = Machine()
    m.bus.write_word(0x9FFFC, 7)
    assert m.bus.read_word(0x9FFFC) == 7

def test_faixa_reservada_rejeitada():
    m = Machine()
    for addr in (0x90000, 0x9FBFC):
        with pytest.raises(IndexError):
            m.bus.read_word(addr)

def test_fora_do_mapa_rejeitado():
    m = Machine()
    with pytest.raises(IndexError):
        m.bus.read_word(0xA0000)