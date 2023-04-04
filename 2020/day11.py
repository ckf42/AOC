import AOCInit
import util
from collections import defaultdict

if __name__ != '__main__':
    exit()

inp = util.getInput(d=11, y=2020)
seatMap = inp.splitlines()
dim = (len(seatMap), len(seatMap[0]))

# part 1
# TODO: ~3s
directions = tuple(complex(*pr) for pr in util.integerLattice(2, 1, util.inf))
seatNeighbour: defaultdict[complex, set[complex]] = defaultdict(set)
occupyStatus: dict[complex, bool] = dict()
for i in range(dim[0]):
    for j in range(dim[1]):
        c = seatMap[i][j]
        pt = complex(i, j)
        if c in 'L#':
            occupyStatus[pt] = (c == '#')
            for d in directions:
                newPt = pt + d
                nPtTp = util.complexToTuple(newPt)
                if all(0 <= pr[0] < pr[1] for pr in zip(nPtTp, dim)) \
                        and seatMap[nPtTp[0]][nPtTp[1]] in 'L#':
                    seatNeighbour[pt].add(newPt)
while True:
    fillCount = {
        pt: sum(occupyStatus[nei] for nei in neiSet)
        for pt, neiSet in seatNeighbour.items()
    }
    toFill = tuple(filter(lambda pt: not occupyStatus[pt] and fillCount[pt] == 0,
                          occupyStatus))
    toEmpty = tuple(filter(lambda pt: occupyStatus[pt] and fillCount[pt] >= 4,
                           occupyStatus))
    if len(toFill) == 0 and len(toEmpty) == 0:
        break
    for pt in toFill:
        occupyStatus[pt] = True
    for pt in toEmpty:
        occupyStatus[pt] = False
print(sum(occupyStatus.values()))

# part 2
# TODO: ~3s
for pt in occupyStatus:
    seatNeighbour[pt].clear()
    ptTuple = util.complexToTuple(pt)
    occupyStatus[pt] = seatMap[ptTuple[0]][ptTuple[1]] == '#'
    for d in directions:
        walkStep = 0
        while True:
            walkStep += 1
            newPt = pt + walkStep * d
            newPtTuple = util.complexToTuple(newPt)
            if not all(0 <= pr[0] < pr[1] for pr in zip(newPtTuple, dim)):
                # outbound
                break
            if newPt in occupyStatus:
                # found
                seatNeighbour[pt].add(newPt)
                break
while True:
    fillCount = {
        pt: sum(occupyStatus[nei] for nei in neiSet)
        for pt, neiSet in seatNeighbour.items()
    }
    toFill = tuple(filter(lambda pt: not occupyStatus[pt] and fillCount[pt] == 0,
                          occupyStatus))
    toEmpty = tuple(filter(lambda pt: occupyStatus[pt] and fillCount[pt] >= 5,
                           occupyStatus))
    if len(toFill) == 0 and len(toEmpty) == 0:
        break
    for pt in toFill:
        occupyStatus[pt] = True
    for pt in toEmpty:
        occupyStatus[pt] = False
print(sum(occupyStatus.values()))


