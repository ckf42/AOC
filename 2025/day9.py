import AOCInit
import util
from functools import cache

if __name__ != "__main__":
    exit()

inp = """\
7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
"""

inp = util.getInput(d=9, y=2025)

pts = [util.getInts(line) for line in inp.splitlines()]
n = len(pts)


# part 1
@cache
def area(pt1, pt2):
    return util.prod(abs(a - b + 1) for a, b in zip(pt1, pt2))


print(max(area(pts[i], pts[j]) for i in range(n) for j in range(i + 1, n)))


# part 2

# minX, minY = min(pt[0] for pt in pts), min(pt[1] for pt in pts)

# def isInside(pt: tuple[int, int]) -> bool:
#     endPoint = (minX - 1, minY - 1)
#     count = 0
#     for i in range(n):
#         res = util.segmentIntersection(
#             *(util.Point.fromIterable(node) for node in (pt, endPoint, pts[i], pts[(i + 1) % n]))
#         )
#         if res is not None:
#             # print(pt, pts[i], pts[(i + 1) % n], "intersect")
#             count += 1
#     # print(pt, count)
#     return count % 2 == 1

# maxArea = -1
# for i in range(n):
#     for j in range(i + 1, n):
#         x, y = pts[i], pts[j]
#         a, b = min(x[0], y[0]), min(x[1], y[1])
#         c, d = max(x[0], y[0]), max(x[1], y[1])
#         valid = True
#         for xx in range(a, c + 1):
#             for yy in range(b, d + 1):
#                 if any(
#                     util.pointOnSegment(
#                         util.Point(xx, yy), util.Point.fromIterable(pts[i]), util.Point.fromIterable(pts[(i + 1) % n])
#                     )
#                     for i in range(n)
#                 ):
#                     continue
#                 if not isInside((xx, yy)):
#                     valid = False
#                     # print(xx, yy, "fail")
#                     break
#             if not valid:
#                 break
#         # print(x, y, valid)
#         if valid:
#             maxArea = max(maxArea, area(x, y))
# print(maxArea)

xlst = [pt[0] for pt in pts]
ylst = [pt[1] for pt in pts]
xValCompressed = {v: i for i, v in enumerate(xlst)}
yValCompressed = {v: i for i, v in enumerate(ylst)}

compressedPts = [(xValCompressed[x], yValCompressed[y]) for x, y in pts]


def realArea(pt1, pt2):
    return area((xlst[pt1[0]], ylst[pt1[1]]), (xlst[pt2[0]], ylst[pt2[1]]))


@cache
def isInside(pt: tuple[int, int]) -> bool:
    endPoint = (-1, -1)
    count = 0
    for i in range(n):
        if pt == compressedPts[i]:
            return True
        if (
            util.segmentIntersection(
                *(
                    util.Point.fromIterable(node)
                    for node in (pt, endPoint, compressedPts[i], compressedPts[(i + 1) % n])
                )
            )
            is not None
        ):
            count += 1
    return count % 2 == 1

# maxArea = -1
# for i in range(n):
#     for j in range(i + 1, n):
#         x, y = compressedPts[i], compressedPts[j]
#         a, b = min(x[0], y[0]), min(x[1], y[1])
#         c, d = max(x[0], y[0]), max(x[1], y[1])
#         valid = True
#         for xx in range(a, c + 1):
#             for yy in range(b, d + 1):
#                 if any(
#                     util.pointOnSegment(
#                         util.Point(xx, yy),
#                         util.Point.fromIterable(compressedPts[idx]),
#                         util.Point.fromIterable(compressedPts[(idx + 1) % n]),
#                     )
#                     for idx in range(n)
#                 ):
#                     continue
#                 if not isInside((xx, yy)):
#                     valid = False
#                     break
#             if not valid:
#                 break
#         if valid:
#             maxArea = max(maxArea, realArea(x, y))
# print(maxArea)
