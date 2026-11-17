from sim.bus import Bus
from sim.memory import Memory
from sim.vram import Vram

def test_vram_render():
    v = Vram()
    v.write_word(0, 0x44434241)
    assert v.render(cols=4, rows=1) == "ABCD"

def test_vram_through_bus():
    bus = Bus()
    vram = Vram()
    bus.attach(0x00000, 0x7FFFF, Memory(0x80000))
    bus.attach(0x80000, 0x8FFFF, vram)
    bus.write_word(0x80000, 0x44434241)
    assert vram.render(cols=4, rows=1) == "ABCD"

def test_vram_nonprintable_is_space():
    v = Vram()
    v.write_word(0, 0x00430041)   # bytes 41 00 43 00
    assert v.render(cols=4, rows=1) == "A C "

def test_vram_render_only_printable_ascii():
    v = Vram()
    v.data[:4] = bytes([31, 32, 126, 127])
    assert v.render(cols=4, rows=1) == "  ~ "