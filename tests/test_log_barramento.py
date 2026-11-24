from sim.bus import Bus
from sim.machine import Machine
from sim.memory import Memory
from sim.programa import PROGRAMA

def test_bus_log():
    bus = Bus()
    bus.trace = True
    bus.attach(0, 0x7FFFF, Memory(0x80000))
    bus.write_word(0x100, 0xAB)
    bus.read_word(0x100)
    assert bus.log == [("WRITE", 0x100, 0xAB), ("READ", 0x100, 0xAB)]

def test_programa_no_barramento():
    m = Machine(n=1000)
    m.bus.trace = True
    m.load(PROGRAMA)
    m.run(30)
    assert ("READ", 0x0, PROGRAMA[0]) in m.bus.log
    assert ("WRITE", 0x80000, 0x364142) in m.bus.log