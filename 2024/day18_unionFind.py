import AOCInit
import util

if __name__ != '__main__':
    exit()

# NOTE:
# this approach is marginally faster than the original binary search
# perhaps due to the target block being among the later half
# more precisely, this takes about double the amount of time of binary search
#     if we enumerate the whole seq of blocks
# if we are using input from https://redd.it/1hgy6nb
#    then this approach is much faster (~5 times) than binary search

inp = util.getInput(d=18, y=2024)
blkSize = 70

w = blkSize + 1
h = blkSize + 1
goal = (blkSize, blkSize)

# part 2
corrupted = tuple(
    util.getInts(line)
    for line in inp.splitlines()
)
n = len(corrupted)
corruptedSet = set(corrupted)
djs = util.DisjointSet(w * h)
visited = set()
for i in range(w):
    for j in range(h):
        if (i, j) in visited or (i, j) in corruptedSet:
            continue
        buff = [(i, j)]
        idx = i * h + j
        while len(buff) != 0:
            x, y = buff.pop()
            if (x, y) in visited:
                continue
            visited.add((x, y))
            djs.union(idx, x * h + y)
            for xx, yy in util.nearby2DGridPts((x, y), (w, h)):
                if (xx, yy) not in corruptedSet:
                    buff.append((xx, yy))
for i in range(n - 1, -1, -1):
    x, y = corrupted[i]
    corruptedSet.remove((x, y))
    for xx, yy in util.nearby2DGridPts((x, y), (w, h)):
        if (xx, yy) not in corruptedSet:
            djs.union(x * h + y, xx * h + yy)
    if djs.isSameGroup(0, blkSize * h + blkSize):
        print(",".join(str(c) for c in corrupted[i]))
        break

