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
datas = list(int(inp[c]) for c in range(0, n, 2))
blanks = list(int(inp[c]) for c in range(1, n, 2))
checksum = 0
dataOffsets = [0] * len(datas)
blankOffsets = [0] * len(blanks)
currOffset = 0
for ptr in range(len(blanks)):
    checksum += ptr * util.rangeSum(range(currOffset, currOffset + datas[ptr]))
    dataOffsets[ptr] = currOffset
    currOffset += datas[ptr]
    blankOffsets[ptr] = currOffset
    currOffset += blanks[ptr]
dataOffsets[-1] = blankOffsets[-1] + blanks[-1]
checksum += len(blanks) * util.rangeSum(range(currOffset, currOffset + datas[-1]))
for ptr in range(len(datas) - 1, 0, -1):
    idx = util.firstIdxSuchThat(blanks, lambda x: x >= datas[ptr], e=ptr)
    if idx is not None:
        checksum -= ptr * datas[ptr] * (dataOffsets[ptr] - blankOffsets[idx])
        blanks[idx] -= datas[ptr]
        blankOffsets[idx] += datas[ptr]
print(checksum)

