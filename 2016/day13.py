import AOCInit
import util
from collections import deque

if __name__ != '__main__':
    exit()

inp = 123

# part 1
wallDict = dict()

def isWall(pt):
    if pt not in wallDict:
        (x, y) = pt
        wallDict[pt] = util.countOnes((x + y) ** 2 + 3 * x + y + inp) & 1 == 1
    return wallDict[pt]

originPt = util.Point.zero(2)

def getNei(pt):
    resList = list()
    for d in util.integerLattice(2, 1):
        newPt = pt + util.Point.fromIterable(d)
        if originPt <= newPt and not isWall(tuple(newPt)):
            resList.append(newPt)
    return resList

initPt = util.Point(1, 1)
goalPt = util.Point(31, 39)
print(util.dijkstra(initPt,
                    lambda nst, ost, oc: oc + 1,
                    getNei,
                    lambda pt: pt == goalPt)[1])

# part 2
distLimit = 50
q: deque[tuple[int, util.Point]] = deque()
q.append((0, initPt))
visited = set()
while len(q) != 0:
    (d, pt) = q.popleft()
    if pt in visited:
        continue
    visited.add(pt)
    if d < distLimit:
        for newPt in getNei(pt):
            q.append((d + 1, newPt))
print(len(visited))

