import AOCInit
import util
import numpy as np
from scipy.signal import convolve2d

if __name__ != '__main__':
    exit()

inp = util.getInput(d=18, y=2018)
dim = 50

initMap = inp.splitlines()
spaces = (np.empty((dim + 2, dim + 2), dtype=np.int8),
          np.empty((dim + 2, dim + 2), dtype=np.int8))
charMap = {'.': 0, '|': 1, '#': 2}
reverseCharMap = {v: k for k, v in charMap.items()}
buffPtr = 0
for j in range(dim + 2):
    for k in (0, 1):
        spaces[k][0, j] = 3
        spaces[k][dim + 1, j] = 3
        spaces[k][j, 0] = 3
        spaces[k][j, dim + 1] = 3
for i in range(1, dim + 1):
    for j in range(1, dim + 1):
        spaces[0][i, j] = charMap[initMap[i - 1][j - 1]]
convKernel = np.ones((3, 3), dtype=np.int8)
convKernel[1, 1] = 0

woodLumbCount = list()
woodLumbCount.append((np.sum(spaces[buffPtr] == 1), np.sum(spaces[buffPtr] == 2)))

# part 1
for _ in range(10):
    woodCount = convolve2d(spaces[buffPtr] == 1, convKernel, mode='same')
    lumbCount = convolve2d(spaces[buffPtr] == 2, convKernel, mode='same')
    for i in range(1, dim + 1):
        for j in range(1, dim + 1):
            if spaces[buffPtr][i, j] == 0:
                # open space
                spaces[1 - buffPtr][i, j] = (1 if woodCount[i, j] >= 3 else 0)
            elif spaces[buffPtr][i, j] == 1:
                # tree space
                spaces[1 - buffPtr][i, j] = (2 if lumbCount[i, j] >= 3 else 1)
            else:
                # lumberyard
                spaces[1 - buffPtr][i, j] = (2 if woodCount[i, j] >= 1 and lumbCount[i, j] >= 1 else 0)
    buffPtr = 1 - buffPtr
    woodLumbCount.append((np.sum(spaces[buffPtr] == 1), np.sum(spaces[buffPtr] == 2)))

# part 2
targetTime = 1000000000
addLoopTime = 900
for _ in range(addLoopTime):
    woodCount = convolve2d(spaces[buffPtr] == 1, convKernel, mode='same')
    lumbCount = convolve2d(spaces[buffPtr] == 2, convKernel, mode='same')
    for i in range(1, dim + 1):
        for j in range(1, dim + 1):
            if spaces[buffPtr][i, j] == 0:
                # open space
                spaces[1 - buffPtr][i, j] = (1 if woodCount[i, j] >= 3 else 0)
            elif spaces[buffPtr][i, j] == 1:
                # tree space
                spaces[1 - buffPtr][i, j] = (2 if lumbCount[i, j] >= 3 else 1)
            else:
                # lumberyard
                spaces[1 - buffPtr][i, j] = (2 if woodCount[i, j] >= 1 and lumbCount[i, j] >= 1 else 0)
    buffPtr = 1 - buffPtr
    woodLumbCount.append((np.sum(spaces[buffPtr] == 1), np.sum(spaces[buffPtr] == 2)))
print(util.prod(util.extrapolatePeriodicSeq(woodLumbCount, targetTime)))
