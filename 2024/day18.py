import AOCInit
import util

import heapq as hq

if __name__ != '__main__':
    exit()

inp = util.getInput(d=18, y=2024)
blkSize = 70

w = blkSize + 1
h = blkSize + 1
goal = (blkSize, blkSize)

# part 1
count = 1024
corrupted = set(
    tuple(util.getInts(line))
    for line in inp.splitlines()[:count]
)
print(util.dijkstra(
        (0, 0),
        lambda nst, ost, oc: oc + 1,
        lambda ost: (pt for pt in util.nearby2DGridPts(ost, (w, h)) if pt not in corrupted),
        lambda st: st == goal
    )[1]
)

# part 2
corrupted = set()
for pt in (tuple(util.getInts(line)) for line in inp.splitlines()):
    corrupted.add(pt)
    buff = [(0, 0)]
    visited = set()
    while len(buff) != 0:
        x, y = buff.pop()
        if (x, y) in visited:
            continue
        visited.add((x, y))
        if (x, y) == goal:
            break
        for nb in util.nearby2DGridPts((x, y), (w, h)):
            if nb not in corrupted and nb not in visited:
                buff.append(nb)
    if goal not in visited:
        print(','.join(str(idx) for idx in pt))
        break

