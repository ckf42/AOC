import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=12, y=2018)

inputBlock = inp.split('\n\n')
toHavePlant = frozenset(int(util.subChar('#.', '10', ls[0]), base=2)
                        for l in inputBlock[1].splitlines()
                        if (ls := l.split())[2] == '#')
assert 0 not in toHavePlant
buffPtr = 0
potThatHasPlant: list[list[int]] = [
        list(tuple(i
                   for i, c in enumerate(inputBlock[0][15:])
                   if c == '#'))
]

# part 1
lbd = [0]
for _ in range(20):
    oldBuffPtr = buffPtr
    buffPtr += 1
    potThatHasPlant.append(list())
    lastPot = -util.inf
    currState = 0
    for potId in potThatHasPlant[oldBuffPtr]:
        # move place for potId
        for shift in range(1, min(5, potId - lastPot)):
            currState = (currState << 1) & 0b11111
            if currState == 0:
                break
            if currState in toHavePlant:
                potThatHasPlant[buffPtr].append(lastPot - 2 + shift)
        # add potId
        currState = ((currState << 1) | 1) & 0b11111
        if currState in toHavePlant:
            potThatHasPlant[buffPtr].append(potId - 2)
        lastPot = potId
    # remainder
    while currState != 0:
        currState = (currState << 1) & 0b11111
        lastPot += 1
        if currState in toHavePlant:
            potThatHasPlant[buffPtr].append(lastPot - 2)
    lbd.append(min(potThatHasPlant[buffPtr]))
print(sum(potThatHasPlant[buffPtr]))

# part 2
additionalRun = 300
for _ in range(additionalRun):
    oldBuffPtr = buffPtr
    buffPtr += 1
    potThatHasPlant.append(list())
    lastPot = -util.inf
    currState = 0
    for potId in potThatHasPlant[oldBuffPtr]:
        # move place for potId
        for shift in range(1, min(5, potId - lastPot)):
            currState = (currState << 1) & 0b11111
            if currState == 0:
                break
            if currState in toHavePlant:
                potThatHasPlant[buffPtr].append(lastPot - 2 + shift)
        # add potId
        currState = ((currState << 1) | 1) & 0b11111
        if currState in toHavePlant:
            potThatHasPlant[buffPtr].append(potId - 2)
        lastPot = potId
    # remainder
    while currState != 0:
        currState = (currState << 1) & 0b11111
        lastPot += 1
        if currState in toHavePlant:
            potThatHasPlant[buffPtr].append(lastPot - 2)
    lbd.append(min(potThatHasPlant[buffPtr]))

calLen = additionalRun + 21
targetTurn = 50000000000
extrapolLbd = util.extrapolatePeriodicSeq(lbd, targetTurn, inDiff=True)
sumSeq = tuple(sum(p - lbd[i] for p in potThatHasPlant[i]) for i in range(calLen))
extrapolSum = util.extrapolatePeriodicSeq(sumSeq, targetTurn)
potCount = tuple(map(len, potThatHasPlant))
extrapolCount = util.extrapolatePeriodicSeq(potCount, targetTurn)
print(extrapolSum + extrapolCount * extrapolLbd)

