import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=6, y=2018)
distLimit = 10000

coorList = tuple(util.getInts(l) for l in inp.splitlines())
bdPts = tuple(map(lambda p: complex(*p),
                  util.transpose(util.rangeBound(util.transpose(coorList)))))
pointList = tuple(map(lambda p: complex(*p), coorList))
l = len(pointList)
directions = tuple(map(lambda p: complex(*p), util.integerLattice(2, 1)))

# part 1
fillCount = [1 for _ in range(l)]
bdReachIdxSet: set[int] = set()
ptToExpand: list[tuple[frozenset[int], complex]] = list((frozenset((i,)), pt)
                                                        for i, pt in enumerate(pointList))
expandedPts = set(pointList)
while len(ptToExpand) != 0:
    belongingDict: dict[complex, set[int]] = dict()
    for idxSet, pt in ptToExpand:
        for d in directions:
            newPt = pt + d
            if newPt in expandedPts:
                continue
            if newPt not in belongingDict:
                belongingDict[newPt] = set()
            belongingDict[newPt].update(idxSet)
    ptToExpand.clear()
    expandedPts.update(belongingDict.keys())
    for pt, idxSet in belongingDict.items():
        if len(idxSet) == 1:
            fillCount[tuple(idxSet)[0]] += 1
        if not (bdPts[0].real <= pt.real <= bdPts[1].real \
                and bdPts[0].imag <= pt.imag <= bdPts[1].imag):
            if len(idxSet) == 1:
                bdReachIdxSet.update(idxSet)
        else:
            ptToExpand.append((frozenset(idxSet), pt))
print(max(fillCount[i] for i in range(l) if i not in bdReachIdxSet))

# part 2
# TODO: need better algorithm other than brute force
regionSize = 0
for i in range(int(bdPts[0].real), int(bdPts[1].real) + 1):
    for j in range(int(bdPts[0].imag), int(bdPts[1].imag) + 1):
        distSum = 0
        for p in coorList:
            distSum += abs(i - p[0]) + abs(j - p[1])
            if distSum >= distLimit:
                break
        if distSum < distLimit:
            regionSize += 1
print(regionSize)

