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
""" # 47 * 590 = 27730
inp = """\
#######
#G..#E#
#E#E.E#
#G.##.#
#...#E#
#...E.#
#######\
""" # 37 * 982 = 36334
inp = util.getInput(d=15, y=2018)

debugPrint = lambda *x: None
# debugPrint = print

caveMap = inp.splitlines()
dim = (len(caveMap), len(caveMap[0]))
elfLoc: list[Optional[complex]] = list(complex(i, j)
              for i in range(dim[0])
              for j in range(dim[1])
              if caveMap[i][j] == 'E')
gobLoc: list[Optional[complex]] = list(complex(i, j)
              for i in range(dim[0])
              for j in range(dim[1])
              if caveMap[i][j] == 'G')
elfCount = len(elfLoc)
gobCount = len(gobLoc)
attackPower = 3
elfHp = list(200 for _ in range(elfCount))
gobHp = list(200 for _ in range(gobCount))
directions = (-1, -1j, 1j, 1)
# loc, isGob, idx in list
locOrderHeap: util.Heap[tuple[complex, bool, int]] = util.MinHeap(
        key=lambda pr: (int(pr[0].real), int(pr[0].imag)))

def printCave():
    elfSet = frozenset((l for l in elfLoc if l is not None))
    gobSet = frozenset((l for l in gobLoc if l is not None))
    print('elf', elfSet)
    print('gob', gobSet)
    for i in range(dim[0]):
        for j in range(dim[1]):
            if caveMap[i][j] == '#':
                print('#', end='')
            else:
                pt = complex(i, j)
                if pt in elfSet:
                    print('E', end='')
                elif pt in gobSet:
                    print('G', end='')
                else:
                    print('.', end='')
        print('')
    print('')

def enemyIdxInRange(pt: complex, isGob: bool) -> Optional[int]:
    minHpIdx = None
    minHp = 0
    for d in directions:
        try:
            currIdx = (elfLoc if isGob else gobLoc).index(pt + d)
            currHp = (elfHp if isGob else gobHp)[currIdx]
            if minHpIdx is None or currHp < minHp:
                minHpIdx = currIdx
                minHp = currHp
        except ValueError:
            pass
    return minHpIdx

def dirToMove(pt: complex, isGob: bool) -> Optional[int]:
    enemySet = frozenset(loc
                         for loc in (elfLoc if isGob else gobLoc)
                         if loc is not None)
    friendSet = frozenset(loc
                          for loc in (gobLoc if isGob else elfLoc)
                          if loc is not None)
    # (dist, loc, source dir)
    h: util.Heap[int, tuple[int, int], int] = util.MinHeap(key=lambda pr: pr[0])
    h.push((0, (int(pt.real), int(pt.imag)), None))
    targetLoc: Optional[tuple[int, int]] = None
    currOptimal = util.inf
    reachedDist: dict[complex, int] = dict()
    sourceDir: defaultdict[complex, list[int]] = defaultdict(list)
    while not h.isEmpty():
        (currDist, currCoor, currDir) = h.pop()
        currLoc = complex(*currCoor)
        # debugPrint('at', currLoc)
        if currDist > currOptimal:
            break
        if currLoc in reachedDist:
            if currDist == reachedDist[currLoc]:
                sourceDir[currLoc].append(currDir)
            continue
        reachedDist[currLoc] = currDist
        sourceDir[currLoc].append(currDir)
        for i in range(4):
            newPt = currLoc + directions[i]
            # debugPrint('checking', newPt)
            (x, y) = (int(newPt.real), int(newPt.imag))
            if not (0 <= x < dim[0]) or not (0 <= y < dim[1]) \
                    or caveMap[x][y] == '#' or newPt in friendSet:
                continue
            if newPt in enemySet:
                # debugPrint('is enemy')
                if currOptimal >= currDist:
                    currOptimal = currDist
                    if targetLoc is None \
                            or currCoor[0] < targetLoc[0] \
                            or (currCoor[0] == targetLoc[0] and currCoor[1] < targetLoc[1]):
                        targetLoc = currCoor
            else:
                h.push((currDist + 1, (x, y), i))
    if targetLoc is None:
        return None
    # debugPrint(targetLoc)
    feasibleDir = set()
    stack = [complex(*targetLoc)]
    # debugPrint(sourceDir)
    while len(stack) != 0:
        # debugPrint(stack)
        loc = stack.pop()
        for dIdx in sourceDir[loc]:
            newLoc = loc - directions[dIdx]
            if newLoc == pt:
                feasibleDir.add(dIdx)
            else:
                stack.append(newLoc)
    return min(feasibleDir)

# part 1

elfRemain = elfCount
gobRemain = gobCount
finishedTurnCount = 0
debugPrint('init')
printCave()
while True:
    debugPrint('starting turn', finishedTurnCount)
    if elfRemain == 0:
        debugPrint('all elf died')
        break
    elif gobRemain == 0:
        debugPrint('all gob died')
        break
    locOrderHeap.extend((elfLoc[idx], False, idx)
                        for idx in range(elfCount)
                        if elfLoc[idx] is not None)
    locOrderHeap.extend((gobLoc[idx], True, idx)
                        for idx in range(gobCount)
                        if gobLoc[idx] is not None)
    while not locOrderHeap.isEmpty():
        (currLoc, isGob, selfIdx) = locOrderHeap.pop()
        if (gobLoc if isGob else elfLoc)[selfIdx] is None:
            continue
        debugPrint('turn for', 'gob' if isGob else 'elf', 'idx', selfIdx, 'at', currLoc)
        attackIdx = enemyIdxInRange(currLoc, isGob)
        if attackIdx is None:
            moveDirIdx = dirToMove(currLoc, isGob)
            if moveDirIdx is not None:
                debugPrint('moving', '^<>v'[moveDirIdx])
                (gobLoc if isGob else elfLoc)[selfIdx] += directions[moveDirIdx]
                attackIdx = enemyIdxInRange(
                        (gobLoc if isGob else elfLoc)[selfIdx],
                        isGob)
        if attackIdx is not None:
            debugPrint('attacking', 'elf' if isGob else 'gob', 'idx', attackIdx)
            if isGob:
                elfHp[attackIdx] -= attackPower
                if elfHp[attackIdx] <= 0:
                    elfLoc[attackIdx] = None
                    elfRemain -= 1
            else:
                gobHp[attackIdx] -= attackPower
                if gobHp[attackIdx] <= 0:
                    gobLoc[attackIdx] = None
                    gobRemain -= 1
        if elfRemain == 0 or gobRemain == 0:
            debugPrint('last killed')
            break
    debugPrint(finishedTurnCount, 'turn end')
    printCave()
    finishedTurnCount += 1
print(finishedTurnCount * sum(hp for hp in elfHp + gobHp if hp > 0))

# part 2
