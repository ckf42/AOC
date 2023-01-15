import AOCInit
import util
from collections import deque
from functools import reduce
from operator import xor

if __name__ != '__main__':
    exit()

inp = util.getInput(d=14, y=2017)

inp = inp.strip()

def knothash(inputStr):
    lenSeq = tuple(map(ord, inputStr)) + (17, 31, 73, 47, 23)
    l = 256
    markString = deque(range(l))
    currPos = 0
    skipSize = 0
    for _ in range(64):
        for opLen in lenSeq:
            markString.rotate(-currPos)
            for i in range(opLen // 2):
                markString[i], markString[opLen - 1 - i] = markString[opLen - 1 - i], markString[i]
            markString.rotate(currPos)
            currPos = (currPos + opLen + skipSize) % l
            skipSize = (skipSize + 1) % l
    return ''.join(map(lambda seg: hex(reduce(xor, seg))[2:].zfill(2),
                       util.splitIntoGp(tuple(markString), 16)))

# part 1
bitDict = {hex(n)[2]: bin(n)[2:].zfill(4) for n in range(16)}
bitMap = set()
for rIdx in range(128):
    h = knothash(inp + f'-{rIdx}')
    for i, c in enumerate(''.join(bitDict[cc] for cc in h)):
        if c == '1':
            bitMap.add(util.Point(rIdx, i))
print(len(bitMap))

# part 2
dirDict = tuple(util.Point.fromIterable(d) for d in util.integerLattice(2, 1))
visited = set()
islandCount = 0
for initPt in bitMap:
    if initPt in visited:
        continue
    islandCount += 1
    stack = [initPt]
    while len(stack) != 0:
        pt = stack.pop()
        if pt in visited:
            continue
        visited.add(pt)
        for d in dirDict:
            newPt = pt + d
            if 0 <= newPt < 128 and newPt in bitMap and newPt not in visited:
                stack.append(newPt)
print(islandCount)

