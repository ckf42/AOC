import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=15, y=2021)

riskMap = tuple(
    tuple(map(int, line))
    for line in inp.splitlines()
)

dimt = (len(riskMap), len(riskMap[0]))
dim = complex(*dimt)
directions = tuple(map(lambda pt: complex(*pt), util.integerLattice(2, 1)))

# part 1
def getNei(pt):
    neiList = list()
    for d in directions:
        newPt = pt + d
        if all(0 <= pr[0] < pr[1]
               for pr in zip(util.complexToTuple(newPt),
                             util.complexToTuple(dim))):
            neiList.append(newPt)
    return neiList

goalPt = dim - complex(1, 1)
print(util.dijkstra(
    initialNode=complex(0, 0),
    costFunc=lambda nst, ost, oc: oc + riskMap[int(nst.real)][int(nst.imag)],
    neighbourListFunc=getNei,
    goalCheckerFunc=lambda pt: pt == goalPt,
    aStarHeuristicFunc=lambda pt: abs((pt - goalPt).real) + abs((pt - goalPt).imag))[1])


# part 2
# ~10s
# TODO: can we speed up with a better astar (that counts block locations)?
def getNewNei(pt):
    neiList = list()
    for d in directions:
        newPt = pt + d
        if all(0 <= pr[0] < pr[1] * 5
               for pr in zip(util.complexToTuple(newPt),
                             util.complexToTuple(dim))):
            neiList.append(newPt)
    return neiList

def newRisk(pt):
    ptt = util.complexToTuple(pt)
    pbs = tuple(divmod(ptt[i], dimt[i]) for i in range(2))
    return (riskMap[pbs[0][1]][pbs[1][1]] + pbs[0][0] + pbs[1][0] - 1) % 9 + 1

goalPt = dim * 5 - complex(1, 1)

print(util.dijkstra(
    initialNode=complex(0, 0),
    costFunc=lambda nst, ost, oc: oc + newRisk(nst),
    neighbourListFunc=getNewNei,
    goalCheckerFunc=lambda pt: pt == goalPt,
    aStarHeuristicFunc=lambda pt: abs((pt - goalPt).real) + abs((pt - goalPt).imag))[1])

