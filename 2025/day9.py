import AOCInit
import util
from functools import cache

if __name__ != "__main__":
    exit()

inp = util.getInput(d=9, y=2025)

pts = [util.getInts(line) for line in inp.splitlines()]
k = len(pts)


# part 1
def area(pt1, pt2):
    return util.prod((abs(pt1[0] - pt2[0]) + 1, abs(pt1[1] - pt2[1]) + 1))


print(max(area(pts[i], pts[j]) for i in range(k) for j in range(i + 1, k)))


# part 2

xlst = sorted(set([pt[0] for pt in pts]))
ylst = sorted(set([pt[1] for pt in pts]))
xValCompressed = {v: i * 2 for i, v in enumerate(xlst)}
yValCompressed = {v: i * 2 for i, v in enumerate(ylst)}
n = len(xlst) * 2
m = len(ylst) * 2

compressedPts = [(xValCompressed[x], yValCompressed[y]) for x, y in pts]


def realArea(pt1, pt2):
    return area((xlst[pt1[0] // 2], ylst[pt1[1] // 2]), (xlst[pt2[0] // 2], ylst[pt2[1] // 2]))


compressedGrid = [[None] * m for _ in range(n)]
for (x1, y1), (x2, y2) in zip(compressedPts, compressedPts[1:] + [compressedPts[0]]):
    if x1 == x2:
        d = 0, (1 if y1 < y2 else -1)
    else:
        d = (1 if x1 < x2 else -1), 0
    compressedGrid[x2][y2] = True
    x, y = x1, y1
    while (x, y) != (x2, y2):
        compressedGrid[x][y] = True
        x += d[0]
        y += d[1]

def isInside(i, j):
    global compressedGrid
    if compressedGrid[i][j] is None:
        total = 0
        for pt1, pt2 in zip(compressedPts, compressedPts[1:] + [compressedPts[0]]):
            insect = util.segmentIntersection(*(util.Point(a, b) for a, b in ((-1, -1), (i, j), pt1, pt2)))
            if insect is None:
                continue
            else:
                total += 1 if insect == util.Point(*pt1) or insect == util.Point(*pt2) else 2
        compressedGrid[i][j] = (total // 2) % 2 == 1
    return compressedGrid[i][j]

maxArea = -1
for i in range(k):
    for j in range(i + 1, k):
        pt1, pt2 = compressedPts[i], compressedPts[j]
        a, b = min(pt1[0], pt2[0]), min(pt1[1], pt2[1])
        c, d = max(pt1[0], pt2[0]), max(pt1[1], pt2[1])
        valid = True
        for x in range(a, c + 1):
            if not isInside(x, b) or not isInside(x, d):
                valid = False
                break
        if valid:
            for y in range(b, d + 1):
                if not isInside(a, y) or not isInside(c, y):
                    valid = False
                    break
        if valid:
            maxArea = max(maxArea, realArea(pt1, pt2))
print(maxArea)

