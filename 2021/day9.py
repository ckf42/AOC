import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=9, y=2021)

heightMap = tuple(tuple(map(int, line))
                  for line in inp.splitlines())
dim = util.Point(len(heightMap), len(heightMap[0]))

directions = tuple(map(util.Point.fromIterable, util.integerLattice(2, 1)))

# part 1
lowPtList = list()
riskLevel = 0
for i in range(dim[0]):
    for j in range(dim[1]):
        pt = util.Point(i, j)
        if all(heightMap[pt[0]][pt[1]] < heightMap[newPt[0]][newPt[1]]
               for d in directions
               if 0 <= (newPt := pt + d) < dim):
            lowPtList.append(pt)
            riskLevel += 1 + heightMap[pt[0]][pt[1]]
print(riskLevel)

# part 2
basinSize = list()
for i, lpt in enumerate(lowPtList):
    visitedPt = set()
    stack = list()
    stack.append(lpt)
    while len(stack) != 0:
        pt = stack.pop()
        if pt in visitedPt:
            continue
        visitedPt.add(pt)
        for d in directions:
            newPt = pt + d
            if 0 <= newPt < dim and heightMap[newPt[0]][newPt[1]] != 9:
                stack.append(newPt)
    basinSize.append(len(visitedPt))
basinSize.sort()
print(util.prod(basinSize[-3:]))
