from sim.machine import Machine

PROGRAM = [
    0x000802B7,   # lui x5, 0x80
    0x04100313,   # addi x6, x0, 0x41
    0x0062A023,   # sw x6, 0(x5)
]

def test_run_prints_every_n(capsys):
    m = Machine(n=3)
    m.load(PROGRAM)
    m.run(3)
    out = capsys.readouterr().out
    assert out.startswith("A   ")

def test_run_silent_before_n(capsys):
    m = Machine(n=1000)
    m.load(PROGRAM)
    m.run(3)
    assert capsys.readouterr().out == ""

def test_program_writes_vram():
    m = Machine(n=1000)
    m.load([
        0x000802B7,   # lui x5, 0x80       (x5 = 0x80000)
        0x04100313,   # addi x6, x0, 0x41  (x6 = 'A')
        0x0062A023,   # sw x6, 0(x5)
    ])
    m.run(3)
    assert m.vram.render(cols=4, rows=1) == "A   "