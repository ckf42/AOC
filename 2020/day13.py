import AOCInit
import util
from sympy.ntheory.modular import crt

if __name__ != '__main__':
    exit()

inp = util.getInput(d=13, y=2020)

# part 1
currTime = int(inp.splitlines()[0])
buses = util.getInts(inp.splitlines()[1])
minBus = buses[0]
waitTime = (-currTime) % buses[0]
for b in buses[1:]:
    wt = (-currTime) % b
    if wt < waitTime:
        minBus = b
        waitTime = wt
print(minBus * waitTime)

# part 2
busConstrain = tuple((m, (-i) % m)
                     for i, c in enumerate(inp.splitlines()[1].split(','))
                     if c != 'x' and (m := int(c)))
print(crt(*util.takeApart(busConstrain))[0])

