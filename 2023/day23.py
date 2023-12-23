import AOCInit
import util

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

# assuming
# this contains all intersect points
# no source (<.>) and no sink (>.<)
# no free space (only confined paths)
nodePos = frozenset(
        (i, j)
        for i in range(dim[0])
        for j in range(dim[1])
        if trailMap[i][j] != '#' \
                and sum(trailMap[nb[0]][nb[1]] != '#'
                        for nb in util.nearby2DGridPts((i, j), dim)) != 2)

nodeLinks: dict[tuple[int, int], dict[tuple[int, int], int]] \
        = {n: dict() for n in nodePos}
for root in nodePos:
    linkStack = [(root, root, 0)]
    while len(linkStack) != 0:
        currPos, prevPos, step = linkStack.pop()
        if currPos in nodePos and currPos != prevPos and currPos != root:
            nodeLinks[root][currPos] = max(nodeLinks[root].get(currPos, 0), step)
            continue
        sym = trailMap[currPos[0]][currPos[1]]
        nextPos: tuple[tuple[int, int], ...] = tuple()
        if sym in slideDir:
            d = slideDir[sym]
            nextPos = ((currPos[0] + d[0], currPos[1] + d[1]),)
        else:
            nextPos = tuple(
                    nb
                    for nb in util.nearby2DGridPts(currPos, dim)
                    if trailMap[nb[0]][nb[1]] != '#')
        for nb in nextPos:
            if nb == prevPos or trailMap[nb[0]][nb[1]] == '#':
                continue
            linkStack.append((nb, currPos, step + 1))

# part 1
# assume DAG
maxDist = 0
stack = [(0, startPos)]
while len(stack) != 0:
    cost, node = stack.pop()
    if node == targetPos:
        maxDist = max(maxDist, cost)
        continue
    for nb, c in nodeLinks[node].items():
        stack.append((cost + c, nb))
print(maxDist)

# part 2
# assume this gives the whole graph
# this can be faster but we only have like 36 nodes
for s in nodePos:
    for e, w in nodeLinks[s].items():
        w = max(w, nodeLinks[e].get(s, w))
        nodeLinks[s][e] = w
        nodeLinks[e][s] = w

# this takes ~1min
# longest path is NP-hard unless graph has good structure
# TODO: optimize?
maxDist = 0
part2Stack: list[tuple[int,
                       tuple[int, int],
                       set[tuple[int, int]]]] = [(0, startPos, set())]
while len(part2Stack) != 0:
    cost, node, visited = part2Stack.pop()
    if node == targetPos:
        maxDist = max(maxDist, cost)
        continue
    for nb, c in nodeLinks[node].items():
        if nb not in visited:
            part2Stack.append((cost + c, nb, visited.union((nb,))))
print(maxDist)

