import AOCInit
import util
import intCode as ic
from collections import defaultdict

if __name__ != '__main__':
    exit()

inp = util.getInput(d=17, y=2019)
code = util.getInts(inp)
prog = ic.IntCode(code)
cameraOutput = ''.join(map(chr, prog.getAllOutput())).strip()
cameraImg = cameraOutput.splitlines()
dim = (len(cameraImg), len(cameraImg[0]))
# ^>v<
directions = (complex(-1, 0), complex(0, 1), complex(1, 0), complex(0, -1))
robotCoor = divmod(util.firstIdxSuchThat(cameraOutput, lambda c: c in '^>v<'),
                   dim[1] + 1)
robotLoc = complex(*robotCoor)

# part 1
def isScaf(loc: complex) -> bool:
    coor = util.complexToTuple(loc)
    return all(pr[0] <= pr[1] < pr[2] for pr in zip((0, 0), coor, dim)) \
            and cameraImg[coor[0]][coor[1]] == '#'

pathTaken: list[str] = list()
currDir = '^>v<'.find(cameraImg[robotCoor[0]][robotCoor[1]])
roadCount: defaultdict[complex, int] = defaultdict(int)
roadCount[robotLoc] = 1
while True:
    dirOffset = util.firstSuchThat(
            (0, -1, 1),
            lambda off: isScaf(robotLoc + directions[(currDir + off) % 4]))[1]
    if dirOffset is None:
        break
    if dirOffset != 0:
        pathTaken.append('L' if dirOffset == -1 else 'R')
    pathTaken.append('1')
    currDir = (currDir + dirOffset) % 4
    robotLoc += directions[currDir]
    roadCount[robotLoc] += 1
print(sum(util.prod(util.complexToTuple(k))
          for k, v in roadCount.items()
          if v > 1))

# part 2
# brute force possible routines, and check if they fit the conditions
# assuming routine always starts with rotating, for better performance
cornerIdx = tuple(i for i, r in enumerate(pathTaken) if r != '1') + (len(pathTaken),)
straightSeg = tuple(''.join(pathTaken[cornerIdx[i]:cornerIdx[i + 1]])
                    for i in range(len(cornerIdx) - 1))
tokenDict: dict[str, int] = dict()
tokenList: list[int] = list()
tokenIdx = 0
for idx, seg in enumerate(straightSeg):
    if seg not in tokenDict:
        tokenDict[seg] = tokenIdx
        tokenIdx += 1
    tokenList.append(tokenDict[seg])
assert tokenIdx in range(ord('z') + 1 - ord('A')), "Too many tokens to encode"
tokenStr = ''.join(map(lambda c: chr(c + ord('A')), tokenList))
tokenToCmd: dict[str, str] = {
        chr(v + ord('A')): k[0] + ',' + str(len(k) - 1)
        for k, v in tokenDict.items()}
routineScheme = None
for aEnd in range(1, len(tokenStr) - 2):
    if routineScheme is not None:
        break
    routineA = tokenStr[:aEnd]
    if aEnd * 4 - 1 > 20:
        break
    for bStart in range(aEnd, len(tokenStr) - 2):
        if routineScheme is not None:
            break
        # tokenStr[aEnd:bStart] must be repetitions of routineA
        if tokenStr[aEnd:bStart] != routineA * ((bStart - aEnd) // len(routineA)):
            continue
        for bEnd in range(bStart + 1, len(tokenStr) - 1):
            if routineScheme is not None:
                break
            routineB = tokenStr[bStart:bEnd]
            if (bEnd - bStart) * 4 - 1 > 20:
                break
            remainParts = frozenset(filter(
                lambda x: x != '',
                tokenStr.replace(routineA, '\n')\
                        .replace(routineB, '\n')\
                        .splitlines()))
            longestPrefix = util.longestCommonPrefix(remainParts)
            # should be repetitions of routineC
            if len(longestPrefix) == 0:
                continue
            for cEnd in range(1, len(longestPrefix) + 1):
                routineC = longestPrefix[:cEnd]
                if cEnd * 4 - 1 > 20:
                    break
                if any(part != routineC * (len(part) // cEnd)
                       for part in remainParts):
                    continue
                compressed = tokenStr.replace(routineA, 'A,')\
                        .replace(routineB, 'B,')\
                        .replace(routineC, 'C,')\
                        .rstrip(',')
                if len(compressed) <= 20:
                    routineScheme = {
                            'main': compressed,
                            'A': ','.join(tuple(tokenToCmd[c] for c in routineA)),
                            'B': ','.join(tuple(tokenToCmd[c] for c in routineB)),
                            'C': ','.join(tuple(tokenToCmd[c] for c in routineC))}
                    break
assert routineScheme is not None, "No routine scheme found"
prog = ic.IntCode((2,) + code[1:])
prog.send(*map(ord, routineScheme['main'] + '\n'))
prog.send(*map(ord, routineScheme['A'] + '\n'))
prog.send(*map(ord, routineScheme['B'] + '\n'))
prog.send(*map(ord, routineScheme['C'] + '\n'))
prog.send(*map(ord, 'n\n'))
print(prog.getAllOutput()[-1])

