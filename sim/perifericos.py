from sim.memory import Memory

class Perifericos(Memory):
    def __init__(self) -> None:
        super().__init__(0x400)