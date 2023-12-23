import AOCInit
import util
from collections import defaultdict

if __name__ != '__main__':
    exit()

inp = util.getInput(d=23, y=2023)

trailMap = inp.splitlines()
dim = (len(trailMap), len(trailMap[0]))
startPos = (0, 1)
targetPos = (dim[0] - 1, dim[1] - 2)
slideDir = {
    '>': (0, 1),
    '<': (0, -1),
    'v': (1, 0),
    '^': (-1, 0),
}

# assume this contains all split points
nodePos = frozenset(
        (i, j)
        for i in range(dim[0])
        for j in range(dim[1])
        if trailMap[i][j] != '#' \
                and sum(trailMap[nb[0]][nb[1]] != '#'
                        for nb in util.nearby2DGridPts((i, j), dim)) != 2)

# part 1
tree = defaultdict(dict)
stack = [(startPos, startPos, (-1, -1), 0)] # curr, prev, root, step from root
while len(stack) != 0:
    currPos, prevPos, root, step = stack.pop()
    if currPos in nodePos:
        tree[root][currPos] = max(tree[root].get(currPos, 0), step)
        root = currPos
        step = 0
    sym = trailMap[currPos[0]][currPos[1]]
    nextPosLst = tuple()
    if sym in slideDir:
        d = slideDir[sym]
        newPos = (currPos[0] + d[0], currPos[1] + d[1])
        nextPosLst = (newPos,)
    else:
        nextPosLst = tuple(
                nb
                for nb in util.nearby2DGridPts(currPos, dim)
                if trailMap[nb[0]][nb[1]] != '#')
    for newPos in nextPosLst:
        if newPos == prevPos:
            continue
        stack.append((newPos, currPos, root, step + 1))

maxDist = 0
h = [(0, startPos)]
while len(h) != 0:
    cost, pos = h.pop()
    if pos == targetPos:
        maxDist = max(maxDist, cost)
        continue
    for n, c in tree[pos].items():
        h.append((c + cost, n))
print(maxDist)


# part 2
# we should be able to build this by adding reverse edges from tree
# not sure about time complexity
flatTree = {pt: dict() for pt in nodePos}
for root in nodePos:
    flatStack = list((nb, root, 1)
                     for nb in util.nearby2DGridPts(root, dim)
                     if trailMap[nb[0]][nb[1]] != '#')  # curr, prev, step
    while len(flatStack) != 0:
        currPos, prevPos, step = flatStack.pop()
        if currPos in nodePos:
            flatTree[root][currPos] = max(step, flatTree[root].get(currPos, 0))
            continue
        for nb in util.nearby2DGridPts(currPos, dim):
            if nb == prevPos or trailMap[nb[0]][nb[1]] == '#':
                continue
            flatStack.append((nb, currPos, step + 1))

# this takes too long (~1min)
# (general) longest path problem seems to be NP(-compete)
# maybe there are optimizations?
maxDist = 0
h = [(0, startPos, set())]
while len(h) != 0:
    cost, pos, visited = h.pop()
    if pos == targetPos:
        maxDist = max(maxDist, cost)
        continue
    for n, c in flatTree[pos].items():
        if n in visited:
            continue
        h.append((c + cost, n, visited.union((n,))))
print(maxDist)
