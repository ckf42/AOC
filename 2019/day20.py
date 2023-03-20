import AOCInit
import util
from typing import Optional
from collections import defaultdict

if __name__ != '__main__':
    exit()

inp = util.getInput(d=20, y=2019)

graphMap = inp.splitlines()
dim = (len(graphMap), len(graphMap[0]))
directions = tuple(complex(*d)
                   for d in util.integerLattice(2, 1))
portalTags: defaultdict[str, list[complex]] = defaultdict(list)
scannedPts: set[complex] = set()
for lLoc in (complex(i, j)
             for i in range(dim[0])
             for j in range(dim[1])
             if graphMap[i][j].isalpha()):
    if lLoc in scannedPts:
        continue
    (ptX, ptY) = util.complexToTuple(lLoc, asInt=True)
    locStack: list[str] = [graphMap[ptX][ptY]]
    portalEntrance: Optional[complex] = None
    ptsToScan: list[complex] = [lLoc]
    while len(ptsToScan) != 0:
        for d in directions:
            newPt = ptsToScan[0] + d
            (x, y) = util.complexToTuple(newPt, asInt=True)
            if not (0 <= x < dim[0] and 0 <= y < dim[1]):
                continue
            m = graphMap[x][y]
            if m in ' #':
                continue
            if m == '.':
                portalEntrance = newPt
            elif m.isupper() and newPt not in scannedPts:
                locStack.append(m)
                ptsToScan.append(newPt)
        scannedPts.add(ptsToScan.pop(0))
    assert len(locStack) == 2 and portalEntrance is not None
    portalTags[''.join(sorted(locStack))].append(portalEntrance)
portals: dict[complex, complex] = {
        l[i]: l[1 - i]
        for l in portalTags.values()
        for i in range(2)
        if len(l) == 2
}

# part 1
def getNei(loc):
    locLst = list()
    if loc in portals:
        locLst.append(portals[loc])
    for d in directions:
        newLoc = loc + d
        (x, y) = util.complexToTuple(newLoc, asInt=True)
        if not (0 <= x < dim[0] and 0 <= y < dim [1]):
            continue
        m = graphMap[x][y]
        if m == '.':
            locLst.append(newLoc)
    return locLst

print(util.dijkstra(initialNode=portalTags['AA'][0],
                    costFunc=(lambda nst, ost, oc: oc + 1),
                    neighbourListFunc=getNei,
                    goalCheckerFunc=(lambda loc: loc == portalTags['ZZ'][0]))[1])


# part 2
# TODO: may be faster if we floodfill paths between portals first
corner = tuple(divmod(x, dim[1] + 1) for x in (inp.find('#'), inp.rfind('#')))
# in: (out, going deeper)
portalWithSides: dict[complex, tuple[complex, bool]] = {
        k: (v, not any(pr[0] == pr[1]
                       for pt in corner
                       for pr in zip(util.complexToTuple(k), pt)))
        for k, v in portals.items()
}
specialPos = (portalTags['AA'][0], portalTags['ZZ'][0])

def getRecurNei(st):
    locLst = list()
    (loc, dep) = st
    if loc in portalWithSides:
        (out, isDeeper) = portalWithSides[loc]
        if isDeeper or dep != 0:
            locLst.append((out, dep + (1 if isDeeper else -1)))
    for d in directions:
        newLoc = loc + d
        (x, y) = util.complexToTuple(newLoc, asInt=True)
        if not (0 <= x < dim[0] and 0 <= y < dim[1]):
            continue
        m = graphMap[x][y]
        if m == '.' and not (dep != 0 and newLoc in specialPos):
            locLst.append((newLoc, dep))
    return locLst

print(util.dijkstra(initialNode=(portalTags['AA'][0], 0),
                    costFunc=(lambda nst, ost, oc: oc + 1),
                    neighbourListFunc=getRecurNei,
                    goalCheckerFunc=(lambda st: st == (portalTags['ZZ'][0], 0)))[1])

