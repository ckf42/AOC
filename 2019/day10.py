import AOCInit
import util
from collections import defaultdict, deque
from math import atan2

if __name__ != '__main__':
    exit()

inp = util.getInput(d=10, y=2019)

inpMap = inp.splitlines()
dim = (len(inpMap), len(inpMap[0]))
ptList = tuple(util.Point(i, j)
               for i in range(dim[0])
               for j in range(dim[1])
               if inpMap[i][j] == '#')
ptIdx = {pt: i for i, pt in enumerate(ptList)}
ptCount = len(ptList)
# idx: {direction: [(multiple, target)]}
lineOfSight: tuple[defaultdict[util.Point, util.Heap[tuple[int, int]]], ...] = tuple(
        defaultdict(util.MinHeap) for pt in ptList)
# O(ptCount ** 2)
for i in range(ptCount - 1):
    for j in range(i + 1, ptCount):
        d = ptList[j] - ptList[i]
        g = abs(util.gcd(*d))
        dd = d // g
        lineOfSight[i][dd].push((g, j))
        lineOfSight[j][-dd].push((g, i))

# part 1
station = lineOfSight[util.argmax(range(ptCount),
                                  lambda idx: len(lineOfSight[idx]))]
print(len(station))

# part 2
dirOrder = deque(sorted(station.keys(),
                        key=lambda pt: atan2(pt[1], pt[0]),
                        reverse=True))
lastVaporized = None
for vaporizedOrder in range(200):
    while len(dirOrder) != 0 and len(station[dirOrder[0]]) == 0:
        dirOrder.popleft()
    assert len(dirOrder) != 0
    lastVaporized = ptList[station[dirOrder[0]].pop()[1]]
    dirOrder.rotate(-1)
assert lastVaporized is not None
print(100 * lastVaporized[1] + lastVaporized[0])

