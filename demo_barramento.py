from sim.machine import Machine
from sim.programa import PROGRAMA

m = Machine(n=1000)
m.bus.trace = True
m.load(PROGRAMA)
m.run(30)
for op, addr, dado in m.bus.log:
    print(f"{op:5}  endereco={addr:#010x}  dado={dado:#010x}")