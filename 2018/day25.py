import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=25, y=2018)

pointList = tuple(util.Point(*util.getInts(l))
                  for l in inp.splitlines())
pointCount = len(pointList)

# part 1
constellation: util.DisjointSet = util.DisjointSet(pointCount)
for i in range(pointCount - 1):
    for j in range(i + 1, pointCount):
        if not constellation.isSameGroup(i, j) and (pointList[i] - pointList[j]).norm(1) <= 3:
            constellation.union(i, j)
print(constellation.groupCount())

# part 2
# no part 2

