import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=10, y=2024)

hikemap = inp.splitlines()
n = len(hikemap)
m = len(hikemap[0])

# part 1
reach: list[list[set[int]]] = [[set() for __ in range(m)] for _ in range(n)]
buff: list[tuple[int, int, int]] = []
counter = 0
for i in range(n):
    for j in range(m):
        if hikemap[i][j] == '9':
            buff.append((i, j, counter))
            counter += 1
while len(buff) != 0:
    i, j, idx = buff.pop()
    c = ord(hikemap[i][j])
    for ii, jj in util.nearby2DGridPts((i, j), (n, m)):
        if ord(hikemap[ii][jj]) == c - 1 \
                and idx not in reach[ii][jj]:
            reach[ii][jj].add(idx)
            buff.append((ii, jj, idx))
res = 0
for i in range(n):
    for j in range(m):
        if hikemap[i][j] != '0':
            continue
        res += len(reach[i][j])
print(res)

# part 2
reachCount: list[list[int]] = [[0] * m for _ in range(n)]
buffPart2 = [(i, j) for i in range(n) for j in range(m) if hikemap[i][j] == '9']
for i, j in buffPart2:
    reachCount[i][j] = 1
while len(buffPart2) != 0:
    i, j = buffPart2.pop()
    c = ord(hikemap[i][j])
    for ii, jj in util.nearby2DGridPts((i, j), (n, m)):
        if ord(hikemap[ii][jj]) == c - 1:
            reachCount[ii][jj] += 1
            buffPart2.append((ii, jj))
res = 0
for i in range(n):
    for j in range(m):
        if hikemap[i][j] != '0':
            continue
        res += reachCount[i][j]
print(res)


