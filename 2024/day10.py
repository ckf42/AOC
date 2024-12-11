import AOCInit
import util

from collections import defaultdict

if __name__ != '__main__':
    exit()

inp = util.getInput(d=10, y=2024)

hikemap = inp.splitlines()
n = len(hikemap)
m = len(hikemap[0])

timer = util.Timer()

# part 1
buff = defaultdict(set)
for i in range(n):
    for j in range(m):
        if hikemap[i][j] == '9':
            buff[(i, j)].add(i * m + j)
for _ in range(9):
    newBuff: defaultdict[tuple[int, int], set[int]] = defaultdict(set)
    for pt, indices in buff.items():
        for ii, jj in util.nearby2DGridPts(pt, (n, m)):
            if ord(hikemap[ii][jj]) == ord(hikemap[pt[0]][pt[1]]) - 1:
                newBuff[(ii, jj)] |= indices
    buff = newBuff
print(sum(len(v) for v in buff.values()))

timer.check()

# part 2
buffPart2 = defaultdict(int)
for i in range(n):
    for j in range(m):
        if hikemap[i][j] == '9':
            buffPart2[(i, j)] = 1
for _ in range(9):
    newBuffPart2: defaultdict[tuple[int, int], int] = defaultdict(int)
    for pt, val in buffPart2.items():
        for ii, jj in util.nearby2DGridPts(pt, (n, m)):
            if ord(hikemap[ii][jj]) == ord(hikemap[pt[0]][pt[1]]) - 1:
                newBuffPart2[(ii, jj)] += val
    buffPart2 = newBuffPart2
print(sum(buffPart2.values()))

timer.stop()

