import AOCInit
import util
from collections import defaultdict

if __name__ != '__main__':
    exit()

inp = util.getInput(d=21, y=2023)

garden = inp.splitlines()
dim = (len(garden), len(garden[0]))
initPos = divmod(inp.index('S'), dim[1] + 1)

# part 1
posSet = frozenset((initPos,))
for _ in range(64):
    posSet = frozenset(
            newPos
            for pos in posSet
            for newPos in util.nearby2DGridPts(pos, dim)
            if garden[newPos[0]][newPos[1]] != '#')
print(len(posSet))

# part 2
# assumptions
# TODO: are these enough?
assert initPos[0] == initPos[1] == dim[0] // 2
assert dim[0] == dim[1]
assert all(garden[i].replace('S', '.') == '.' * dim[0]
           for i in (0, -1, initPos[0]))
assert all(''.join(line[i] for line in garden).replace('S', '.') == '.' * dim[0]
           for i in (0, -1, initPos[0]))

targetStep = 26501365
n, gpIdx = divmod(targetStep, dim[0])

history = [1]
posSet = frozenset((initPos,))
# faster?
for _ in range(dim[0] * 2 + gpIdx):
    posSet = frozenset(
            newPos
            for pos in posSet
            for newPos in util.nearby2DGridPts(pos)
            if garden[newPos[0] % dim[0]][newPos[1] % dim[1]] != '#')
    history.append(len(posSet))

# assume that each takeFromEvery(history, dim[0], i) is a quad func
# of form a + b n + c n^2
# with a, b, c possibly distinct for each i
# TODO: prove this without fiddling with data
data = util.takeFromEvery(history, dim[0], gpIdx)
assert len(data) >= 3
a = data[0]
c = util.diff(data, 2)[0] // 2
b = data[1] - a - c
print(a + b * n + c * n ** 2)

