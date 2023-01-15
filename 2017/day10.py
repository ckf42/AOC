import AOCInit
import util
from collections import deque
from functools import reduce

if __name__ != '__main__':
    exit()

inp = util.getInput(d=10, y=2017)
l = 256

# part 1
lenSeq = util.getInts(inp)
markString = deque(range(l))
currPos = 0
skipSize = 0
for opLen in lenSeq:
    opLen = lenSeq[skipSize]
    markString.rotate(-currPos)
    for i in range(opLen // 2):
        markString[i], markString[opLen - 1 - i] = markString[opLen - 1 - i], markString[i]
    markString.rotate(currPos)
    currPos = (currPos + opLen + skipSize) % l
    skipSize += 1
print(markString[0] * markString[1])

# part 2
lenSeq = tuple(map(ord, inp.strip())) + (17, 31, 73, 47, 23)
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
print(''.join(map(lambda seg: hex(reduce(lambda x, y: x ^ y, seg))[2:].zfill(2),
                  util.splitIntoGp(tuple(markString), 16))))

