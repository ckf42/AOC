import AOCInit
import util
import re
from typing import NamedTuple, Optional

if __name__ != '__main__':
    exit()

inp = util.getInput(d=24, y=2018)

class Gp(NamedTuple):
    unitCount: int
    hp: int
    attack: int
    init: int
    weak: frozenset[str]
    immu: frozenset[str]
    dmgType: str

# read only data
weaknessRe = re.compile(r'weak to (.*?)[;\)]')
immuneRe = re.compile(r'\(immune to (.*?)[;\)]')
dmgTypeRe = re.compile(r'does \d+ (\w+) damage')
gpStat = tuple(tuple(Gp(*util.getInts(l),
                        frozenset(t for p in weaknessRe.findall(l) for t in p.split(', ')),
                        frozenset(t for p in immuneRe.findall(l) for t in p.split(', ')),
                        dmgTypeRe.search(l).group(1))
                     for l in block.splitlines()[1:])
               for block in inp.split('\n\n'))
gpCount = list(map(len, gpStat))

# read-write data
remainUnit = list(list(gp.unitCount for gp in side) for side in gpStat)
isChosen = list(list(False for gp in side) for side in gpStat)
immuBuff = 0

# (sideIdx, gpIdx), order by (eff power, init)
# using MinHeap as MaxHeap does not work well with non-float key
selectOrderHeap: util.Heap[tuple[int, int]] = util.MinHeap(
        key=lambda item: (-(remainUnit[item[0]][item[1]] * \
                (gpStat[item[0]][item[1]].attack + immuBuff * (1 - item[0]))),
                          -gpStat[item[0]][item[1]].init))
# (sideIdx, gpIdx, targetIdx), order by init
attackOrderHeap: util.Heap[tuple[int, int, int]] = util.MaxHeap(
        key=lambda item: gpStat[item[0]][item[1]].init)

while True:
    remainUnit[:] = list(list(gp.unitCount for gp in side) for side in gpStat)
    isChosen[:] = list(list(False for gp in side) for side in gpStat)
    hasUnitLost = True
    while all(any(c > 0 for c in side) for side in remainUnit) \
            and hasUnitLost:
        hasUnitLost = False
        # target selection
        selectOrderHeap.clear()
        for sideIdx in (0, 1):
            for gpIdx in range(gpCount[sideIdx]):
                isChosen[sideIdx][gpIdx] = False
                if remainUnit[sideIdx][gpIdx] > 0:
                    selectOrderHeap.push((sideIdx, gpIdx))
        attackOrderHeap.clear()
        while not selectOrderHeap.isEmpty():
            (sideIdx, gpIdx) = selectOrderHeap.pop()
            targetIdx: Optional[int] = None
            # damage, eff power, init
            currTarget: Optional[tuple[int, int, int]] = None
            selfStat = gpStat[sideIdx][gpIdx]
            for idx in range(gpCount[1 - sideIdx]):
                if (remainCount := remainUnit[1 - sideIdx][idx]) > 0 \
                        and not isChosen[1 - sideIdx][idx] \
                        and selfStat.dmgType not in (target := gpStat[1 - sideIdx][idx]).immu:
                    targetSpec = (
                            (2 if selfStat.dmgType in target.weak else 1),
                            remainCount * (target.attack + immuBuff * sideIdx),
                            target.init)
                    if targetIdx is None or targetSpec > currTarget:
                        targetIdx = idx
                        currTarget = targetSpec
            if targetIdx is not None:
                isChosen[1 - sideIdx][targetIdx] = True
                attackOrderHeap.push((sideIdx, gpIdx, targetIdx))
        # attack
        while not attackOrderHeap.isEmpty():
            (sideIdx, gpIdx, targetIdx) = attackOrderHeap.pop()
            assert targetIdx is not None
            if remainUnit[sideIdx][gpIdx] <= 0:
                continue
            selfStat = gpStat[sideIdx][gpIdx]
            unitLost = (
                    (2
                     if selfStat.dmgType in gpStat[1 - sideIdx][targetIdx].weak
                     else 1) \
                             * remainUnit[sideIdx][gpIdx] \
                             * (gpStat[sideIdx][gpIdx].attack + immuBuff * (1 - sideIdx))) \
                             // gpStat[1 - sideIdx][targetIdx].hp
            if unitLost > 0:
                remainUnit[1 - sideIdx][targetIdx] -= unitLost
                hasUnitLost = True
    # part 1
    if immuBuff == 0:
        print(sum(gp for side in remainUnit for gp in side if gp > 0))
    # part 2
    if any(c > 0 for c in remainUnit[1]):
        immuBuff += 1
    else:
        print(sum(c for c in remainUnit[0] if c > 0))
        break


