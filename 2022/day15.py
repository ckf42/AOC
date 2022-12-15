import AOCInit
import util
from sympy import Interval, Union

if __name__ != '__main__':
    exit()

inp = tuple(util.splitIntoGp(util.getInts(l), 2)
            for l in util.getInput(d=15, y=2022).splitlines())

def dist(p1, p2):
    return sum(abs(p1[i] - p2[i]) for i in range(2))

sensorRad = tuple((p[0], dist(*p)) for p in inp)

# part 1
rowNum = 2000000
def getImpossibleRange(targetY):
    return Union(*(Interval(sr[0][0] - r, sr[0][0] + r)
                   for sr in sensorRad
                   if (r := sr[1] - abs(sr[0][1] - targetY)) >= 0))
print(getImpossibleRange(rowNum))


# part 2
coorBd = 4000000
searchBegin = 0 # 3253551
for targetY in util.inclusiveRange(searchBegin, coorBd):
    bdyX = tuple((sr[0][0] - r - 1, sr[0][0] + r + 1)
                 for sr in sensorRad
                 if (r := sr[1] - abs(sr[0][1] - targetY)) >= 0)
    possibleX = set(filter(
        lambda x: (0 <= x <= coorBd) and all(dist((x, targetY), sr[0]) > sr[1]
                                             for sr in sensorRad),
        util.flatten(bdyX)))
    if len(possibleX) != 0:
        for x in possibleX:
            print((x, targetY), x * 4000000 + targetY)
        break

