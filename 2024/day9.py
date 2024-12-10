import AOCInit
import util

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
for i in range(n):
    if (i ^ 1) & 1:
        checksum += (i // 2) * util.rangeSum(range(currOffset, currOffset + blocks[i]))
    offsets[i] = currOffset
    currOffset += blocks[i]
for i in range(n - 1, 1, -2):
    idx = util.firstIdxSuchThat(blocks, lambda x: x >= blocks[i], s=1, e=i, step=2)
    if idx is not None:
        checksum -= (i // 2) * blocks[i] * (offsets[i] - offsets[idx])
        blocks[idx] -= blocks[i]
        offsets[idx] += blocks[i]
print(checksum)

