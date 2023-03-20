import AOCInit
import util
from collections import defaultdict
from math import ceil
from graphlib import TopologicalSorter

if __name__ != '__main__':
    exit()

inp = util.getInput(d=14, y=2019)

def toDesc(entry):
    sEnt = entry.split(' ')
    return (int(sEnt[0]), sEnt[1])

formulas = {
        resp[1]: (resp[0], tuple(map(toDesc, ps[0].split(', '))))
        for l in inp.splitlines()
        if (ps := l.split(' => ')) and (resp := toDesc(ps[1]))}
ts = TopologicalSorter({k: tuple(map(lambda x: x[1], v[1]))
                        for k, v in formulas.items()})
enumOrder = list(ts.static_order())[::-1]
assert enumOrder[-1] == 'ORE' # san check
enumOrder.pop()

# part 1
def getNeededOre(fuelCount):
    req = defaultdict(int)
    req['FUEL'] = fuelCount
    for item in enumOrder:
        repeatCount = ceil(req[item] / formulas[item][0])
        for quan, ingred in formulas[item][1]:
            req[ingred] += quan * repeatCount
    return req['ORE']

print(getNeededOre(1))

# part 2
oreMax = 1000000000000
bounds = [1, None]
while bounds[1] is None or bounds[1] - bounds[0] != 1:
    m = (bounds[0] * 2) if bounds[1] is None else (sum(bounds) // 2)
    if getNeededOre(m) > oreMax:
        bounds[1] = m
    else:
        bounds[0] = m
print(bounds[0])
