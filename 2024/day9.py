import AOCInit
import util

import heapq as hq

if __name__ != '__main__':
    exit()

inp = util.getInput(d=9, y=2024).strip()

blocks = list(int(c) for c in inp)
n = len(blocks)

# part 1
checksum = 0
currOffset = blocks[0]
blankPtr = 1
dataPtr = n - 1
dataId = dataPtr // 2
while blankPtr < dataPtr:
    blkToMove = min(blocks[blankPtr], blocks[dataPtr])
    checksum += dataId * util.rangeSum(range(currOffset, currOffset + blkToMove))
    currOffset += blkToMove
    blocks[blankPtr] -= blkToMove
    blocks[dataPtr] -= blkToMove
    if blocks[blankPtr] == 0:
        blockLen = blocks[blankPtr + 1]
        checksum += (blankPtr + 1) // 2 * util.rangeSum(range(currOffset, currOffset + blockLen))
        currOffset += blockLen
        blankPtr += 2
    if blocks[dataPtr] == 0:
        dataId -= 1
        dataPtr -= 2
print(checksum)


# part 2
blocks = list(int(c) for c in inp)
checksum = 0
offsets = [0] * n
currOffset = 0
locs = [list() for _ in range(10)]
for i in range(n):
    if (i ^ 1) & 1:
        checksum += (i // 2) * util.rangeSum(range(currOffset, currOffset + blocks[i]))
    elif blocks[i] != 0:
        locs[blocks[i]].append(i)
    offsets[i] = currOffset
    currOffset += blocks[i]
for i in range(1, 10):
    hq.heapify(locs[i])
for i in range(n - 1, 1, -2):
    rightBlankSize = -1
    for blankSize in range(blocks[i], 10):
        if len(locs[blankSize]) != 0 and locs[blankSize][0] > i:
            locs[blankSize].clear()
        if len(locs[blankSize]) != 0:
            if rightBlankSize == -1 or locs[blankSize][0] < locs[rightBlankSize][0]:
                rightBlankSize = blankSize
    if rightBlankSize != -1:
        blankIdx = hq.heappop(locs[rightBlankSize])
        checksum -= (i // 2) * blocks[i] * (offsets[i] - offsets[blankIdx])
        blocks[blankIdx] -= blocks[i]
        offsets[blankIdx] += blocks[i]
        if blocks[blankIdx] != 0:
            hq.heappush(locs[blocks[blankIdx]], blankIdx)
print(checksum)

