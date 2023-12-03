import AOCInit
import util
from collections import defaultdict

if __name__ != '__main__':
    exit()

inp = util.getInput(d=3, y=2023)
scheme = inp.splitlines()
n, m = len(scheme), len(scheme[0])

nearbyNums = defaultdict(list)
nearbySyms = defaultdict(list)  # in case one num is next to multiple syms
for i in range(n):
    for j in range(m):
        if scheme[i][j].isdigit() or scheme[i][j] == '.':
            continue
        visited = set()
        for nb in util.nearby2DGridPts((i, j), bd=(n, m), isL1=False):
            if not scheme[nb[0]][nb[1]].isdigit() or nb in visited:
                continue
            s, e = nb[1], nb[1] + 1
            while s >= 0 and scheme[nb[0]][s].isdigit():
                s -= 1
            while e < m and scheme[nb[0]][e].isdigit():
                e += 1
            for k in range(s + 1, e):
                visited.add((nb[0], k))
            nearbyNums[(i, j)].append(int(scheme[nb[0]][s + 1:e]))
            nearbySyms[(nb[0], s + 1)].append((i, j))

def parseInt(i, j):
    e = j + 1
    while e < m and scheme[i][e].isdigit():
        e += 1
    return int(scheme[i][j:e])

# part 1
print(sum(parseInt(*pt) for pt in nearbySyms.keys()))


# part 2
print(sum(util.prod(nums)
          for (symPos, nums) in nearbyNums.items()
          if scheme[symPos[0]][symPos[1]] == '*' \
                  and len(nums) == 2))


