import AOCInit
import util
import re

if __name__ != '__main__':
    exit()

chipRe = re.compile(r'\b(\w+)-compatible microchip', re.I)
genRe = re.compile(r'\b(\w+) generator', re.I)

inp = util.getInput(d=11, y=2016).splitlines()
floorContents = tuple((chipRe.findall(l), genRe.findall(l)) for l in inp) # chip, gen
itemIdxDict = {n: i for i, n in enumerate(set(util.flatten(floorContents, level=2)))}
itemCount = len(itemIdxDict)
initState = [0] + [None] * (2 * itemCount)
for i in range(4):
    for cIdx in map(lambda n: itemIdxDict[n], floorContents[i][0]):
        initState[cIdx * 2 + 1] = i
    for rIdx in map(lambda n: itemIdxDict[n], floorContents[i][1]):
        initState[rIdx * 2 + 2] = i

def isValidState(state):
    iCount = (len(state) - 1) // 2
    unpairedItems = tuple(filter(lambda i: state[i * 2 + 1] != state[i * 2 + 2],
                                 range(iCount)))
    return all(all(state[i] != state[j]
                   for j in unpairedItems
                   if i != j)
               for i in unpairedItems)

def getNei(state):
    transList = list()
    eleLoc = state[0]
    mState = list(state)
    iCount = (len(state) - 1) // 2
    movableIndices = tuple(filter(lambda i: state[i] == eleLoc,
                                  range(1, 1 + 2 * iCount)))
    mLen = len(movableIndices)
    for mi in range(mLen):
        for mj in range(mi, mLen):
            (i, j) = (movableIndices[mi], movableIndices[mj])
            # move item i and j
            if eleLoc > 0:
                mState[0] = mState[i] = mState[j] = eleLoc - 1
                if isValidState(mState):
                    transList.append(tuple(mState))
                mState[0] = mState[i] = mState[j] = eleLoc
            if eleLoc < 3:
                mState[0] = mState[i] = mState[j] = eleLoc + 1
                if isValidState(mState):
                    transList.append(tuple(mState))
                mState[0] = mState[i] = mState[j] = eleLoc
    return transList

# part 1
print(util.dijkstra(initialNode=tuple(initState),
                    costFunc=lambda ns, st, oc: oc + 1,
                    neighbourListFunc=getNei,
                    goalCheckerFunc=lambda st: all(loc == 3 for loc in st),
                    aStarHeuristicFunc=lambda st: sum(3 - loc for loc in st) // 2)[1])

# part 2
# took 1.8 GM RAM and ~10 min without answer
# initState += [0] * 4
# print(util.dijkstra(initialNode=tuple(initState),
                    # costFunc=lambda ns, st, oc: oc + 1,
                    # neighbourListFunc=getNei,
                    # goalCheckerFunc=lambda st: all(loc == 3 for loc in st),
                    # aStarHeuristicFunc=lambda st: sum(3 - loc for loc in st) // 2)[1])

