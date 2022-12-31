import AOCInit
import util
from bisect import bisect_right

if __name__ != '__main__':
    exit()

inp = util.getInput(d=22, y=2016)

# pt, used, avail
nodes = tuple((util.Point(il[0], il[1]), il[3], il[4])
              for l in inp.strip().splitlines()[2:]
              if (il := util.getInts(l)))
nCount = len(nodes)

# part 1
usedSpace = sorted(tuple(nodes[i][1]
                         for i in range(len(nodes))
                         if nodes[i][1] != 0))
availSpace = sorted(tuple(nodes[i][2]
                          for i in range(len(nodes))),
                    reverse=True)
viaCount = 0
for avail in availSpace:
    if avail < usedSpace[0]:
        break
    viaCount += bisect_right(usedSpace, avail)
viaCount -= util.count(nodes, lambda n: 0 != n[1] <= n[2])

print(viaCount)

# part 2
# for a in range(nCount):
    # for b in range(nCount):
        # if a != b and nodes[a][1] != 0 and nodes[a][1] <= nodes[b][2]:
            # print(nodes[a], nodes[b])
# b always seems to be an empty disk
# layoutDim = util.Point(*map(max, util.takeApart(tuple(n[0] for n in nodes))))
# emptyDisks = tuple(n[0] for n in nodes if n[1] == 0)
# directions = tuple(util.Point(*d) for d in util.integerLattice(2, 1))
# assert len(emptyDisks) == 1
# targetLoc = util.Point(layoutDim[0], 0)

# def getNei(st):
    # resList = list()
    # (blankPt, dataPt) = st
    # for d in directions:
        # newPt = blankPt + d
        # if not (0 <= newPt < layoutDim) or :
            # continue

    # return resList


# # blank pt, target loc
# print(util.dijkstra((emptyDisks[0], targetLoc),
                    # lambda nst, ost, oc: oc + 1,
                    # getNei,
                    # lambda st: st[1] == util.Point(0, 0)))

