import AOCInit
import util
from sympy import Interval, Union

if __name__ != '__main__':
    exit()

inp = tuple(util.splitIntoGp(util.getInts(l), 2)
            for l in util.getInput(d=15, y=2022).splitlines())

def dist(p1, p2):
    return sum(abs(p1[i] - p2[i]) for i in range(2))

(sensor, beacon, radius) = util.takeApart(tuple((*p, dist(*p)) for p in inp))
sLen = len(sensor)

# part 1
rowNum = 2000000
forbidXRange = Union(*(Interval(sensor[i][0] - r, sensor[i][0] + r)
                       for i in range(sLen)
                       if (r := radius[i] - abs(sensor[i][1] - rowNum)) >= 0))
print(forbidXRange.measure + len(forbidXRange.boundary) // 2 \
      - util.count(set(beacon),
                   lambda b: b[1] == rowNum and b[0] in forbidXRange))


# part 2
coorBd = 4000000
upward = set()
downward = set()
for i in range(sLen - 1):
    for j in range(i + 1, sLen):
        if dist(sensor[i], sensor[j]) == radius[i] + radius[j] + 2:
            upward.update(set.intersection(*({sensor[k][1] - sensor[k][0] + s * (radius[k] + 1)
                                              for s in (-1, 1)}
                                             for k in (i, j))))
            downward.update(set.intersection(*({sensor[k][1] + sensor[k][0] + s * (radius[k] + 1)
                                                for s in (-1, 1)}
                                               for k in (i, j))))
for u in upward:
    for d in downward:
        pt = ((d - u) // 2, (u + d) // 2)
        if all(0 <= c <= coorBd for c in pt) \
                and all(dist(sensor[i], pt) > radius[i] for i in range(sLen)):
            print(pt, pt[0] * 4000000 + pt[1])

