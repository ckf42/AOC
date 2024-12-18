import AOCInit
import util

import bisect

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
def isDisconnected(blocks: set[tuple[int, int]]) -> bool:
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
            if nb not in blocks and nb not in visited:
                buff.append(nb)
    return goal not in visited

allCorrupted = tuple(
        util.getInts(line)
        for line in inp.splitlines()
)
n = len(allCorrupted)
breakIdx = bisect.bisect_left(
    range(n),
    True,
    key=lambda idx: isDisconnected(set(allCorrupted[:idx + 1]))
)
print(','.join(str(x) for x in allCorrupted[breakIdx]))

