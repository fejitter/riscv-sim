from sim.machine import Machine
from sim.programa import PROGRAMA

def test_programa_completo():
    m = Machine(n=1000)
    m.load(PROGRAMA)
    m.run(30)
    assert m.cpu.rf.read(1) == 0x42
    assert m.cpu.rf.read(4) == 6          
    assert m.ram.read_word(0x1000) == 6
    assert m.cpu.rf.read(7) == 0x360000
    assert m.vram.render(cols=4, rows=1) == "BA6 "
    assert m.cpu.pc == 0x48