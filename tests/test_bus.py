import pytest
from sim.bus import Bus
from sim.memory import Memory

def test_bus_routes_to_ram():
    bus = Bus()
    bus.attach(0x00000, 0x7FFFF, Memory(0x80000))
    bus.write_word(0x100, 0xABCD)
    assert bus.read_word(0x100) == 0xABCD

def test_bus_unmapped_raises():
    bus = Bus()
    bus.attach(0x00000, 0x7FFFF, Memory(0x80000))
    with pytest.raises(IndexError):
        bus.read_word(0x90000)    # faixa reservada