import AOCInit
import util

from collections import deque

if __name__ != '__main__':
    exit()


inp = util.getInput(d=20, y=2024)
timeSaveLimit = 100

sCoor = inp.index('S')
eCoor = inp.index('E')

grid = inp.splitlines()
n = len(grid)
m = len(grid[0])
s = divmod(sCoor, m + 1)
e = divmod(eCoor, m + 1)

visitCostFromStart = dict()
q = deque([(0, s)])
while len(q) != 0:
    cost, pt = q.popleft()
    if pt in visitCostFromStart:
        continue
    visitCostFromStart[pt] = cost
    if pt == e:
        continue
    q.extend((
        (cost + 1, nb)
        for nb in util.nearby2DGridPts(pt, (n, m))
        if grid[nb[0]][nb[1]] != '#'
    ))
normalCost = visitCostFromStart[e]


visitCostFromEnd = dict()
q = deque([(0, e)])
while len(q) != 0:
    cost, pt = q.popleft()
    if pt in visitCostFromEnd:
        continue
    visitCostFromEnd[pt] = cost
    if pt == s:
        continue
    q.extend((
        (cost + 1, nb)
        for nb in util.nearby2DGridPts(pt, (n, m))
        if grid[nb[0]][nb[1]] != '#'
    ))

# part 1
count = sum(
    1
    for pt1, cost1 in visitCostFromStart.items()
    for offset in util.integerLattice(2, 2)
    if cost1 + visitCostFromEnd.get((pt1[0] + offset[0], pt1[1] + offset[1]), normalCost) \
                + abs(offset[0]) + abs(offset[1]) <= normalCost - timeSaveLimit
)
print(count)

# part 2
count = sum(
    1
    for pt1, cost1 in visitCostFromStart.items()
    for offset in util.integerLattice(2, 20)
    if cost1 + visitCostFromEnd.get((pt1[0] + offset[0], pt1[1] + offset[1]), normalCost) \
                + abs(offset[0]) + abs(offset[1]) <= normalCost - timeSaveLimit
)
print(count)

