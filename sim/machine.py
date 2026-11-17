from sim.bus import Bus
from sim.cpu import CPU
from sim.memory import Memory
from sim.vram import Vram

class Machine:
    def __init__(self, n: int = 100) -> None:
        self.ram = Memory(0x80000)
        self.vram = Vram()
        self.bus = Bus()
        self.bus.attach(0x00000, 0x7FFFF, self.ram)
        self.bus.attach(0x80000, 0x8FFFF, self.vram)
        self.cpu = CPU(self.bus)
        self.n = n

    def load(self, words: list[int]) -> None:
        for i, w in enumerate(words):
            self.ram.write_word(i * 4, w)

    def run(self, max_steps: int) -> None:
        for count in range(1, max_steps + 1):
            self.cpu.step()
            if count % self.n == 0:
                print(self.vram.render())