import AOCInit
import util
import numpy as np

if __name__ != '__main__':
    exit()

inp = np.array(tuple(tuple(map(int, l))
                     for l in util.getInput(d=8, y=2022).splitlines()),
               dtype=np.intc)
dim = len(inp)

# part 1
# ~ (4 + 1) d^2 time, ~ d^2 space
visibleTrees = np.full((dim, dim), False, dtype=bool)
for i in range(dim):
    leftMax = -float('Inf')
    rightMax = -float('Inf')
    for j in range(dim):
        if inp[i, j] > leftMax:
            visibleTrees[i, j] = True
            leftMax = inp[i, j]
        if inp[i, dim - 1 - j] > rightMax:
            visibleTrees[i, dim - 1 - j] = True
            rightMax = inp[i, dim - 1 - j]
    leftMax = -float('Inf')
    rightMax = -float('Inf')
    for j in range(dim):
        if inp[j, i] > leftMax:
            visibleTrees[j, i] = True
            leftMax = inp[j, i]
        if inp[dim - 1 - j, i] > rightMax:
            visibleTrees[dim - 1 - j, i] = True
            rightMax = inp[dim - 1 - j, i]
print(np.sum(visibleTrees))

# part 2
# ~ (4 * 2 + 1) d^2 time, ~ d^2 + d space
score = np.full((dim, dim), 1, dtype=np.intc)
score[:, 0] = 0
score[:, dim - 1] = 0
score[0, :] = 0
score[dim - 1, :] = 0
prevMax = np.empty((dim, ), dtype=np.intc)
for i in range(1, dim - 1):
    prevMax[0] = 0
    for j in range(1, dim - 1):
        pm = j - 1
        while pm > 0 and inp[i, j] > inp[i, pm]:
            pm = prevMax[pm]
        prevMax[j] = pm
        score[i, j] *= j - prevMax[j]
    prevMax[0] = 0
    for j in range(1, dim - 1):
        pm = j - 1
        while pm > 0 and inp[j, i] > inp[pm, i]:
            pm = prevMax[pm]
        prevMax[j] = pm
        score[j, i] *= j - prevMax[j]
    prevMax[dim - 1] = dim - 1
    for j in range(dim - 2, -1, -1):
        pm = j + 1
        while pm < dim - 1 and inp[i, j] > inp[i, pm]:
            pm = prevMax[pm]
        prevMax[j] = pm
        score[i, j] *= prevMax[j] - j
    prevMax[dim - 1] = dim - 1
    for j in range(dim - 2, -1, -1):
        pm = j + 1
        while pm < dim - 1 and inp[j, i] > inp[pm, i]:
            pm = prevMax[pm]
        prevMax[j] = pm
        score[j, i] *= prevMax[j] - j
print(np.max(score))

