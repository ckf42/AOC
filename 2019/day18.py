import AOCInit
import util
from collections import defaultdict
from functools import cache

if __name__ != '__main__':
    exit()

inp = util.getInput(d=18, y=2019)

@cache
def toMask(c: str) -> int:
    return 1 << (ord(c) - ord('a'))

graphMap = inp.splitlines()
dim = (len(graphMap), len(graphMap[0]))
initPos = complex(*divmod(inp.find('@'), dim[1] + 1))
keyPos = {k: complex(*divmod(inp.find(k), dim[1] + 1))
          for k in filter(str.islower, inp)}
allKeySum = sum(map(toMask, keyPos.keys()))
directions = tuple(complex(*d)
                   for d in util.integerLattice(2, 1))
keyList = ''.join(keyPos.keys())

# part 1
# TODO: ~11s
# (start key): {(end key): (key req, dist)}
reachableKeys: defaultdict[str, defaultdict[str, list[tuple[int, int]]]] = defaultdict(
        lambda: defaultdict(list))
# location, key used, dist
pathStack: list[tuple[complex, int, int]] = list()
# location: {key used to get here: cost}
visitedStates: defaultdict[complex, dict[int, int]] = defaultdict(dict)
for keyToEnum in '@' + keyList:
    pathStack.clear()
    pathStack.append((keyPos.get(keyToEnum, initPos), 0, 0))
    visitedStates.clear()
    if keyToEnum != '@':
        reachableKeys[keyToEnum][keyToEnum].append((0, 0))
    while len(pathStack) != 0:
        (loc, keyUsed, currDist) = pathStack.pop()
        if loc in visitedStates \
                and any(keyUsed & k == k and currDist >= d
                        for k, d in visitedStates[loc].items()):
            continue
        visitedStates[loc][keyUsed] = currDist
        for d in directions:
            newLoc = loc + d
            (x, y) = tuple(map(int, (newLoc.real, newLoc.imag)))
            if not (0 <= x < dim[0] and 0 <= y < dim[1]):
                continue
            m = graphMap[x][y]
            if m == '#':
                continue
            if m in keyList \
                    and all(dist > currDist + 1
                            for (req, dist) in reachableKeys[keyToEnum][m]
                            if req & keyUsed == req):
                # have not reach here with fewer keys and shorter dist
                reachableKeys[keyToEnum][m].append((keyUsed, currDist + 1))
            pathStack.append((newLoc,
                              keyUsed | (toMask(m.lower())
                                         if m.isupper()
                                         else 0),
                              currDist + 1))
    if keyToEnum != '@':
        reachableKeys[keyToEnum].pop(keyToEnum)
# currMark: {targetMark: heuristicCost}
heuristicCost: dict[str, dict[str, int]] = {
    k: {m: min(map(lambda x: x[1], pr)) for m, pr in vd.items()}
    for k, vd in reachableKeys.items()
}
# (dist, mark, keyGot)
distHeap: util.Heap[tuple[int, str, int]] = util.MinHeap(runtimeKeyOnly=True)
distHeap.push((0, '@', 0), key=0)
# (mark, keyGot)
visited: set[tuple[str, int]] = set()
while not distHeap.isEmpty():
    (dist, mark, keyGot) = distHeap.pop()
    if (mark, keyGot) in visited:
        continue
    if keyGot == allKeySum:
        print(dist)
        break
    visited.add((mark, keyGot))
    for nextMark, pathList in reachableKeys[mark].items():
        for keyReq, d in pathList:
            if (msk := toMask(nextMark)) & keyGot == 0 and keyGot & keyReq == keyReq:
                distHeap.push(
                        (dist + d, nextMark, keyGot | msk),
                        key=dist + d + max((hv
                                            for m, hv in heuristicCost[nextMark].items()
                                            if toMask(m) & keyGot == 0),
                                           default=0))

# part 2
# ~3s
(x, y) = (int(initPos.real), int(initPos.imag))
graphMap[x - 1] = ''.join(
        {y - 1: '0', y: '#', y + 1: '1'}.get(i, graphMap[x - 1][i])
        for i in range(dim[1]))
graphMap[x] = ''.join(
        ('#' if y - 1 <= i <= y + 1 else graphMap[x][i])
        for i in range(dim[1]))
graphMap[x + 1] = ''.join(
        {y - 1: '2', y: '#', y + 1: '3'}.get(i, graphMap[x + 1][i])
        for i in range(dim[1]))
robotInitPos = tuple(initPos + d
                     for d in (-1 - 1j, -1 + 1j, 1 - 1j, 1 + 1j))
reachableKeys.clear()
for keyToEnum, searchPos in zip('0123' + keyList,
                                robotInitPos + tuple(keyPos.values())):
    pathStack.clear()
    pathStack.append(((keyPos[keyToEnum]
                       if keyToEnum in keyList
                       else robotInitPos[int(keyToEnum)]), 0, 0))
    visitedStates.clear()
    if keyToEnum.isalpha():
        reachableKeys[keyToEnum][keyToEnum].append((0, 0))
    while len(pathStack) != 0:
        (loc, keyUsed, currDist) = pathStack.pop()
        if loc in visitedStates \
                and any(keyUsed & k == k and currDist >= d
                        for k, d in visitedStates[loc].items()):
            continue
        visitedStates[loc][keyUsed] = currDist
        for d in directions:
            newLoc = loc + d
            (x, y) = tuple(map(int, (newLoc.real, newLoc.imag)))
            if not (0 <= x < dim[0] and 0 <= y < dim[1]):
                continue
            m = graphMap[x][y]
            if m == '#':
                continue
            if m in keyList \
                    and all(dist > currDist + 1
                            for (req, dist) in reachableKeys[keyToEnum][m]
                            if req & keyUsed == req):
                    # have not reach here with fewer keys and shorter dist
                reachableKeys[keyToEnum][m].append((keyUsed, currDist + 1))
            pathStack.append((newLoc,
                              keyUsed | (toMask(m.lower())
                                         if m.isupper()
                                         else 0),
                              currDist + 1))
    if keyToEnum.isalpha():
        reachableKeys[keyToEnum].pop(keyToEnum)
# currMark: {targetMark: heuristicCost}
heuristicCost = {
    k: {m: min(map(lambda x: x[1], pr)) for m, pr in vd.items()}
    for k, vd in reachableKeys.items()
}
# (dist, marks, keyGot)
distHeap.clear()
distHeap.push((0, '0123', 0), key=0)
# (mark, keyGot)
visited.clear()
while not distHeap.isEmpty():
    (dist, mark, keyGot) = distHeap.pop()
    if (mark, keyGot) in visited:
        continue
    if keyGot == allKeySum:
        print(dist)
        break
    visited.add((mark, keyGot))
    markList = list(mark)
    for rIdx in range(4):
        for nextMark, pathList in reachableKeys[mark[rIdx]].items():
            markList[rIdx] = nextMark
            for keyReq, d in pathList:
                if (msk := toMask(nextMark)) & keyGot == 0 \
                        and keyGot & keyReq == keyReq:
                    distHeap.push(
                            (dist + d, ''.join(markList), keyGot | msk),
                            key=dist + d + sum(max(
                                (hv
                                 for m, hv in heuristicCost[nMark].items()
                                 if toMask(m) & keyGot == 0),
                                default=0)
                                               for nMark in markList))
            markList[rIdx] = mark[rIdx]

