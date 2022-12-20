import AOCInit
import util
import re
from collections import deque
import itertools as it

if __name__ != '__main__':
    exit()

inp = util.getInput(d=11, y=2016)

chipRe = re.compile(r'\b(\w+)-compatible microchip', re.I)
genRe = re.compile(r'\b(\w+) generator', re.I)
floorContents = tuple((chipRe.findall(l), genRe.findall(l)) for l in inp.splitlines())
itemIdx = {n: i
           for i, n in enumerate(set(util.flatten(floorContents, 2)))}
itemCount = len(itemIdx)
initArrangement = [None] * (2 * itemCount)
for flrIdx, flr in enumerate(floorContents):
    for idx, itemList in enumerate(flr):
        for item in itemList:
            initArrangement[2 * itemIdx[item] + idx] = flrIdx
assert all(flr is not None for flr in initArrangement)

def isValidState(stateSeq):
    return all(stateSeq[2 * itemIdx] == stateSeq[2 * itemIdx + 1] \
            or all(stateSeq[2 * itemIdx + 1] == stateSeq[2 * otherIdx + 1]
                   for otherIdx in range(len(stateSeq) // 2)
                   if stateSeq[2 * itemIdx + 1] == stateSeq[2 * otherIdx])
               for itemIdx in range(len(stateSeq) // 2))

def toFloorState(stateSeq):
    return tuple(sorted(util.splitIntoGp(stateSeq, 2), reverse=True))

def getNeiSeq(st, currFloor):
    resList = list()
    itemsToMove = tuple(filter(lambda idx: st[idx] == currFloor,
                               range(len(st))))
    mSt = list(st)
    for delta in (d for d in (1, -1) if 0 <= currFloor + d < 4):
        newFloor = currFloor + delta
        for moveIdx in it.chain(it.combinations(itemsToMove, 2),
                                it.combinations(itemsToMove, 1)):
            for idx in moveIdx:
                mSt[idx] = newFloor
            if isValidState(mSt):
                resList.append((newFloor, tuple(mSt)))
            for idx in moveIdx:
                mSt[idx] = currFloor
    return resList

# double bfs
def getMinMoveCount(initArr):
    # state: (cost, curr floor, floor states)
    startQueue = deque(((0, 0, toFloorState(initArr)),))
    endQueue = deque(((0, 3, ((3, 3),) * (len(initArr) // 2)),))
    visitedFromStart = dict() # (curr floor, floor states): min cost
    visitedFromEnd = dict()
    optimalStates = None
    while True:
        # start
        while len(startQueue) != 0 and startQueue[0][1:] in visitedFromStart:
            startQueue.popleft()
        if len(startQueue) == 0:
            break
        # print("start", len(startQueue))
        (currCost, currFlr, flrState) = startQueue.popleft()
        visitedFromStart[(currFlr, flrState)] = currCost
        if (currFlr, flrState) in visitedFromEnd:
            # found
            optimalStates = (currFlr, flrState)
            break
        # extend
        st = util.flatten(flrState) # type 1 chip, type 1 gen, type 2 chip, ...
        mSt = list(st)
        currCost += 1
        for newFlr, nst in getNeiSeq(st, currFlr):
            startQueue.append((currCost, newFlr, toFloorState(nst)))
        # end
        while len(endQueue) != 0 and endQueue[0][1:] in visitedFromEnd:
            endQueue.popleft()
        if len(endQueue) == 0:
            break
        # print("end", len(endQueue))
        (currCost, currFlr, flrState) = endQueue.popleft()
        visitedFromEnd[(currFlr, flrState)] = currCost
        if (currFlr, flrState) in visitedFromStart:
            # found
            optimalStates = (currFlr, flrState)
            break
        # extend
        st = util.flatten(flrState) # type 1 chip, type 1 gen, type 2 chip, ...
        mSt = list(st)
        currCost += 1
        for newFlr, nst in getNeiSeq(st, currFlr):
            endQueue.append((currCost, newFlr, toFloorState(nst)))
    if optimalStates is not None:
        return visitedFromStart[optimalStates] + visitedFromEnd[optimalStates]

# part 1
print(getMinMoveCount(initArrangement))

# part 2
initArrangement += [0, 0, 0, 0]
print(getMinMoveCount(initArrangement))

