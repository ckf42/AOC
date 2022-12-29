import AOCInit
import util
from hashlib import md5

if __name__ != '__main__':
    exit()

passcode = util.getInput(d=17, y=2016).strip()

directions = ((-1, 0), (1, 0), (0, -1), (0, 1))
dirDesc = 'UDLR'
doorStateDict = dict()

def getDoorState(p):
    if p not in doorStateDict:
        h = md5((passcode + p).encode()).hexdigest()[:4]
        doorStateDict[p] = tuple(c in 'bcdef' for c in h)
    return doorStateDict[p]

def getNextState(state):
    resList = list()
    (pt, p) = state
    doorState = getDoorState(p)
    for i in range(4):
        d = directions[i]
        newPt = tuple(pt[i] + d[i] for i in range(2))
        if not all(0 <= newPt[i] < 4 for i in range(2)):
            continue
        if doorState[i]:
            resList.append((newPt, p + dirDesc[i]))
    return resList

# part 1
minPath = None
maxPathLen = -float('Inf')
stack = list()
stack.append(((0, 0), ''))
while len(stack) != 0:
    (pt, p) = stack.pop()
    if pt == (3, 3):
        if minPath is None or len(minPath) > len(p):
            minPath = p
        maxPathLen = max(maxPathLen, len(p))
        continue
    for newSt in getNextState((pt, p)):
        stack.append(newSt)
print(minPath)

# part 2
print(maxPathLen)


