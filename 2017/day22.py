import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=22, y=2017)

blockMap = inp.splitlines()
dim = (len(blockMap), len(blockMap[0]))
initLoc = dim[0] // 2 + (dim[1] // 2) * 1j
directions = (-1, 1j, 1, -1j) # L <-> R

# part 1
loc = initLoc
currDir = 0
pointStateDict: dict[complex, int] = dict()
for i in range(dim[0]):
    for j in range(dim[1]):
        if blockMap[i][j] == '#':
            pointStateDict[i + j * 1j] = 1
infectBurstCount = 0
for _ in range(10000):
    if loc in pointStateDict:
        currDir = (currDir + 1) % 4
        pointStateDict.pop(loc)
    else:
        currDir = (currDir - 1) % 4
        pointStateDict[loc] = 1
        infectBurstCount += 1
    loc = loc + directions[currDir]
print(infectBurstCount)

# part 2
loc = initLoc
currDir = 0
# no: clean, 1: weak, 2: infect, 3: flag
pointStateDict = dict()
for i in range(dim[0]):
    for j in range(dim[1]):
        if blockMap[i][j] == '#':
            pointStateDict[i + j * 1j] = 2
infectBurstCount = 0
for _ in range(10000000):
    ptState = pointStateDict.get(loc, 0)
    currDir = (currDir - 1 + ptState) % 4
    if ptState == 3:
        pointStateDict.pop(loc)
    else:
        if ptState == 1:
            infectBurstCount += 1
        pointStateDict[loc] = ptState + 1
    loc = loc + directions[currDir]
print(infectBurstCount)


