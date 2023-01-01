import AOCInit
import util
from collections import namedtuple
from bisect import bisect_right

if __name__ != '__main__':
    exit()

inp = util.getInput(d=22, y=2016)

Disk = namedtuple('Disk', ['total', 'used', 'avail'])
# pt: used, avail
nodes = {util.Point(il[0], il[1]): Disk(il[2], il[3], il[4])
         for l in inp.strip().splitlines()[2:]
         if (il := util.getInts(l))}
nCount = len(nodes)

# part 1
usedSpace = sorted(tuple(ua.used
                         for ua in nodes.values()
                         if ua.used != 0))
availSpace = sorted(tuple(ua.avail
                          for ua in nodes.values()),
                    reverse=True)
viaCount = 0
for avail in availSpace:
    if avail < usedSpace[0]:
        break
    viaCount += bisect_right(usedSpace, avail)
viaCount -= util.count(nodes.values(), lambda n: 0 != n.used <= n.avail)

print(viaCount)

# part 2
# for viable pair, b always seems to be an empty disk
coorMax = util.Point(*map(max, util.takeApart(tuple(nodes.keys()))))
emptyDisks = tuple(pt for pt, ua in nodes.items() if ua.used == 0)
assert len(emptyDisks) == 1
emptyDiskLoc = emptyDisks[0]
targetDataLoc = util.Point(coorMax[0], 0)

directions = tuple(util.Point(*d) for d in util.integerLattice(2, 1))

# def getNei(state):
    # resList = list()
    # (emptyLoc, dataLoc) = state
    # for d in directions:
        # newPt = emptyLoc + d
        # if not (0 <= newPt <= coorMax):
            # continue
    # return resList

