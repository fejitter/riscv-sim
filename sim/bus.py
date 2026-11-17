class Bus:
    def __init__(self) -> None:
        self.devices = []   # lista de (inicio, fim, dispositivo)

    def attach(self, start: int, end: int, device) -> None:
        self.devices.append((start, end, device))

    def _find(self, addr: int):
        for start, end, dev in self.devices:
            if start <= addr <= end:
                return start, dev
        raise IndexError(f"endereço sem dispositivo: {addr:#x}")

    def read_word(self, addr: int) -> int:
        start, dev = self._find(addr)
        return dev.read_word(addr - start)   # endereço relativo ao dispositivo

    def write_word(self, addr: int, value: int) -> None:
        start, dev = self._find(addr)
        dev.write_word(addr - start, value)