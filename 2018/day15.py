import AOCInit
import util
from typing import Optional
from collections import defaultdict

if __name__ != '__main__':
    exit()

inp = """\
#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######\
"""
# inp = util.getInput(d=15, y=2018)

caveMap = inp.splitlines()
dim = util.Point(len(caveMap), len(caveMap[0]))
elfLoc = list(util.MutPoint(i, j)
              for i in range(dim[0])
              for j in range(dim[1])
              if caveMap[i][j] == 'E')
elfCount = len(elfLoc)
elfHp = list(200 for _ in range(elfCount))
gobLoc = list(util.MutPoint(i, j)
              for i in range(dim[0])
              for j in range(dim[1])
              if caveMap[i][j] == 'G')
gobCount = len(gobLoc)
gobHp = list(200 for _ in range(gobCount))
# idx in list, coor, isGob
moveOrder: util.Heap[tuple[util.Point, int, bool]] = util.MinHeap(key=None)
neighDir = (util.Point(-1, 0), util.Point(0, -1), util.Point(0, 1), util.Point(1, 0))
# reverse dir: 3 - dIdx
attackPower = 3

def enemyIdxInRange(pt: util.Point, isGob: bool) -> tuple[int, ...]:
    return tuple((elfLoc if isGob else gobLoc).index(newPt)
                 for i in range(4)
                 if ((newPt := pt + neighDir[i]) or True) \
                         and 0 <= newPt < dim \
                         and caveMap[newPt[0]][newPt[1]] != '#' \
                         and newPt in (elfLoc if isGob else gobLoc))

def dirToMove(pt: util.Point, isGob: bool) -> Optional[int]:
    elfSet = frozenset(map(util.Point.fromIterable, (l for l in elfLoc if l is not None)))
    gobSet = frozenset(map(util.Point.fromIterable, (l for l in gobLoc if l is not None)))
    # find possible target
    sourceDir: defaultdict[util.Point, list[int]] = defaultdict(list)
    reachedDist: dict[util.Point, int] = dict()
    possibleTarget: set[util.Point] = set()
    distToTarget = util.inf
    # dist, pt, sourceDir
    h: util.Heap[tuple[int, util.Point, int]] = util.MinHeap(((0, pt, -1),), key=None)
    while not h.isEmpty():
        (currDist, currPt, sDir) = h.pop()
        if currPt in reachedDist:
            if currDist == reachedDist[currPt]:
                # also a possible path, but no need to search again
                sourceDir[currPt].append(sDir)
            continue
        if currDist > distToTarget:
            # already enumerated all necessary points
            break
        reachedDist[currPt] = currDist
        sourceDir[currPt].append(3 - sDir) # points to source
        for dIdx in range(4):
            newPt = currPt + neighDir[dIdx]
            if not (0 <= newPt < dim) \
                    or caveMap[newPt[0]][newPt[1]] == '#' \
                    or newPt in (gobSet if isGob else elfSet):
                # blocked
                continue
            if newPt in (elfSet if isGob else gobSet):
                # enemy
                possibleTarget.add(currPt)
                distToTarget = currDist
            else:
                h.push((currDist + 1, newPt, dIdx))
    if len(possibleTarget) == 0:
        return None
    # backtrack to pt
    target = min(possibleTarget)
    feasibleDir = set()
    stack: list[tuple[int, util.Point]] = list()
    stack.extend(((d, target) for d in sourceDir[target]))
    while len(stack) != 0:
        (d, loc) = stack.pop()
        if loc == pt:
            feasibleDir.add(3 - d)
            if len(feasibleDir) == 4:
                # all directions are possible, no need to keep checking
                break
        else:
            newLoc = loc + neighDir[d]
            stack.extend((((dd, newLoc) for dd in sourceDir[newLoc])))
    return min(feasibleDir)

def printCave():
    for i in range(dim[0]):
        for j in range(dim[1]):
            if caveMap[i][j] == '#':
                print('#', end='')
            else:
                pt = util.Point(i, j)
                if pt in elfLoc:
                    print('E', end='')
                elif pt in gobLoc:
                    print('G', end='')
                else:
                    print('.', end='')
        print('')
    print('')



# part 1
turnCount = 0
while elfCount != 0 and gobCount != 0:
    turnCount += 1
    print(turnCount)
    printCave()
    moveOrder.extend(tuple((util.Point(*elfLoc[idx]), idx, False)
                           for idx in range(elfCount)
                           if elfLoc[idx] is not None))
    moveOrder.extend(tuple((util.Point(*gobLoc[idx]), idx, True)
                           for idx in range(gobCount)
                           if gobLoc[idx] is not None))
    while not moveOrder.isEmpty():
        (_, entIdx, isGob) = moveOrder.pop()
        if (gobLoc if isGob else elfLoc)[entIdx] is None:
            continue
        attackIdxList = enemyIdxInRange((gobLoc if isGob else elfLoc)[entIdx], isGob)
        if len(attackIdxList) == 0:
            mvDir = dirToMove(util.Point.fromIterable((gobLoc if isGob else elfLoc)[entIdx]),
                              isGob)
            if mvDir is not None:
                (gobLoc if isGob else elfLoc)[entIdx] += neighDir[mvDir]
                attackIdxList = enemyIdxInRange((gobLoc if isGob else elfLoc)[entIdx], isGob)
        if len(attackIdxList) != 0:
            targetIdx = util.argmin(attackIdxList,
                                    lambda i: (elfHp if isGob else gobHp)[i])
            (elfHp if isGob else gobHp)[targetIdx] -= attackPower
            if (elfHp if isGob else gobHp)[targetIdx] <= 0:
                # died
                if isGob:
                    elfLoc[targetIdx] = None
                    elfCount -= 1
                else:
                    gobLoc[targetIdx] = None
                    gobCount -= 1



# part 2


