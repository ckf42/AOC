import AOCInit
import util
import numpy as np

if __name__ != '__main__':
    exit()

inp = util.getInput(d=3, y=2018)

# part 1
claimDict = {
    ls[0]: (ls[1], ls[2], ls[1] + ls[3], ls[2] + ls[4])
    for l in inp.splitlines()
    if (ls := util.getInts(l))
}
land = np.zeros((1000, 1000), dtype=np.uint16)
for claim in claimDict.values():
    land[claim[0]:claim[2], claim[1]:claim[3]] += 1
print(np.sum(land >= 2))

# part 2
assert 0 not in claimDict
land[:, :] = 0
claimingUnclaimed = set()
for cIdx, claim in claimDict.items():
    if (prevClaimer := frozenset(land[claim[0]:claim[2], claim[1]:claim[3]].flatten())) == {0}:
        claimingUnclaimed.add(cIdx)
    else:
        for claimer in prevClaimer:
            if claimer != 0:
                claimingUnclaimed.discard(claimer)
    land[claim[0]:claim[2], claim[1]:claim[3]] = cIdx
print(claimingUnclaimed.pop())

