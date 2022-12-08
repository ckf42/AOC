import AOCInit
import util
import numpy as np
from scipy import signal

if __name__ != '__main__':
    exit()

inp = util.getInput(d=18, y=2015).splitlines()
originalBoard = np.array(tuple(util.sub(('#', '.'), (1, 0), l) for l in inp), dtype=bool)

stencil = np.ones((3, 3), dtype=np.int8)
stencil[1, 1] = 0

# part 1
steps = 100
board = originalBoard.copy()
for i in range(steps):
    nei = signal.convolve2d(board, stencil, mode='same')
    np.logical_or(nei == 3, np.logical_and(nei == 2, board), out=board)
print(np.sum(board))

# part 2
originalBoard[0, 0] = originalBoard[0, -1] = originalBoard[-1, 0] = originalBoard[-1, -1] = True
for i in range(steps):
    nei = signal.convolve2d(originalBoard, stencil, mode='same')
    np.logical_or(nei == 3, np.logical_and(nei == 2, originalBoard), out=originalBoard)
    originalBoard[0, 0] = originalBoard[0, -1] = originalBoard[-1, 0] = originalBoard[-1, -1] = True
print(np.sum(originalBoard))

