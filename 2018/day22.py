import AOCInit
import util
from functools import cache

if __name__ != '__main__':
    exit()

inp = util.getInput(d=22, y=2018)
(dep, tarX, tarY) = util.getInts(inp)
# (dep, tarX, tarY) = (510, 10, 10)

def eroFromGeoIdx(geoIdx):
    return (geoIdx + dep) % 20183

@cache
def getGeoIdx(x, y):
    if (x, y) == (0, 0) or (x, y) == (tarX, tarY):
        return 0
    if x == 0:
        return y * 48271
    if y == 0:
        return x * 16807
    return eroFromGeoIdx(getGeoIdx(x - 1, y)) * eroFromGeoIdx(getGeoIdx(x, y - 1))

@cache
def erosionLevel(x, y):
    return eroFromGeoIdx(getGeoIdx(x, y)) % 3

# part 1
print(sum(erosionLevel(i, j) for i in range(tarX + 1) for j in range(tarY + 1)))


# part 2
directions = tuple(util.integerLattice(2, 1))

# 0: rocky, neither
# 1: wet, torch
# 2: narrow, climb
# x, y, equip
def transit(st):
    stateList = list()
    currErosion = erosionLevel(st[0], st[1])
    if not st[3]:
        stateList.append((st[0], st[1],
                          3 - st[2] - currErosion,
                          True))
    for d in directions:
        (newX, newY) = tuple(st[i] + d[i] for i in range(2))
        if newX >= 0 and newY >= 0:
            nbErosion = erosionLevel(newX, newY)
            if nbErosion != st[2]:
                stateList.append((newX, newY,
                                  st[2],
                                  (currErosion == nbErosion) and st[3]))
    return stateList

print(util.dijkstra(
    (0, 0, 1, False),
    lambda nst, ost, oc: oc + (7 if ost[2] != nst[2] else 1),
    transit,
    lambda st: st[:3] == (tarX, tarY, 1),
    lambda st: (abs(st[0] - tarX) + abs(st[1] - tarY)) + (7 if st[2] != 1 else 0))[1])




