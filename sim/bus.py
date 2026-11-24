class Bus:
    def __init__(self) -> None:
        self.devices = []   
        self.trace = False  
        self.log = []       

    def attach(self, start: int, end: int, device) -> None:
        self.devices.append((start, end, device))

    def _find(self, addr: int):
        for start, end, dev in self.devices:
            if start <= addr <= end:
                return start, dev
        raise IndexError(f"endereço sem dispositivo: {addr:#x}")

    def read_word(self, addr: int) -> int:
        start, dev = self._find(addr)
        value = dev.read_word(addr - start)
        if self.trace:
            self.log.append(("READ", addr, value))
        return value

    def write_word(self, addr: int, value: int) -> None:
        start, dev = self._find(addr)
        dev.write_word(addr - start, value)
        if self.trace:
            self.log.append(("WRITE", addr, value & 0xFFFFFFFF))


# log fica desligado por padrão para não crescer sem limite em programas longos