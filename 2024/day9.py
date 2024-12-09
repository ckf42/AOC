import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=9, y=2024).strip()

blocks = list(int(c) for c in inp)
data = list(blocks[0::2])
blank = list(blocks[1::2])

# part 1
checksum = 0
blankPtr = 0
currPtr = data[0]
while blankPtr < len(data) - 1:
    blkToMove = min(blank[blankPtr], data[-1])
    checksum += (2 * currPtr + blkToMove - 1) * blkToMove // 2 * (len(data) - 1)
    blank[blankPtr] -= blkToMove
    data[-1] -= blkToMove
    currPtr += blkToMove
    if data[-1] == 0:
        data.pop()
    if blank[blankPtr] == 0:
        blankPtr += 1
        checksum += (currPtr * 2 + data[blankPtr] - 1) * data[blankPtr] // 2 * blankPtr
        currPtr += data[blankPtr]
print(checksum)


# part 2
ptr = 0
checksum = 0
currPtr = 0
blankOffsets = []
dataOffsets = []
while ptr < len(blocks):
    dataOffsets.append(currPtr)
    checksum += (currPtr * 2 + blocks[ptr] - 1) * blocks[ptr] // 2 * (ptr // 2)
    currPtr += blocks[ptr]
    blankOffsets.append(currPtr)
    ptr += 1
    if ptr < len(blocks):
        currPtr += blocks[ptr]
        ptr += 1
data = list(blocks[0::2])
blank = list(blocks[1::2])
ndata = len(data)
for i in range(ndata - 1, 0, -1):
    idx = util.firstIdxSuchThat(blank, lambda x: x >= data[i], e=i)
    if idx is not None:
        blank[idx] -= data[i]
        checksum -= i * (dataOffsets[i] - blankOffsets[idx]) * data[i]
        blankOffsets[idx] += data[i]
print(checksum)

