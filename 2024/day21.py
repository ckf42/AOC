import AOCInit
import util

import heapq as hq
from collections import defaultdict

if __name__ != '__main__':
    exit()

inp = util.getInput(d=21, y=2024)

instLines = inp.splitlines()

moveSig = {
        (1, 0): 'v',
        (-1, 0): '^',
        (0, 1): '>',
        (0, -1): '<'
}

numpadMap = """\
789
456
123
 0A
""".splitlines()
controllerMap = """\
 ^A
<v>
""".splitlines()

def getEdges(splittedMap: list[str]) -> dict[str, dict[str, str]]:
    n = len(splittedMap)
    m = len(splittedMap[0])
    return {
            splittedMap[i][j]: {
                moveSig[(ni - i, nj - j)]: splittedMap[ni][nj]
                for ni, nj in util.nearby2DGridPts((i, j), (n, m))
                if splittedMap[ni][nj] != ' '
            }
            for i in range(n)
            for j in range(m)
            if splittedMap[i][j] != ' '
    }

numpadEdges = getEdges(numpadMap)
controllerEdges = getEdges(controllerMap)

def getMoveSeq(
        edges: dict[str, dict[str, str]]
        ) -> dict[str, defaultdict[str, list[str]]]:
    moveSeq: dict[str, defaultdict[str, list[str]]] = dict()
    for startKey in edges:
        moveSeq[startKey] = defaultdict(list)
        h = [(0, "", startKey)]
        costDict: dict[str, int] = dict()
        while len(h) != 0:
            cost, seq, key = hq.heappop(h)
            if costDict.get(key, cost + 1) < cost:
                continue
            costDict[key] = cost
            moveSeq[startKey][key].append(seq + 'A')
            for move, nextKey in edges[key].items():
                hq.heappush(h, (
                    cost + (10 if len(seq) == 0 or move != seq[-1] else 1),
                    seq + move,
                    nextKey
                ))
    return moveSeq

numpadMoveSeq = getMoveSeq(numpadEdges)
controllerMoveSeq = getMoveSeq(controllerEdges)

def getFinalKeyPressDict(middleRobotCount):
    controllerMoveLen = {
        sKey: {
            eKey: 1
            for eKey in controllerEdges
        }
        for sKey in controllerEdges
    }
    for _ in range(middleRobotCount):
        controllerMoveLen = {
            sKey: {
                eKey: min(sum(
                        controllerMoveLen[a][b]
                        for a, b in zip('A' + seq[:-1], seq)
                    ) for seq in seqs)
                for eKey, seqs in v.items()
            }
            for sKey, v in controllerMoveSeq.items()
        }
    return {
        sKey: {
            eKey: min(sum(
                    controllerMoveLen[a][b]
                    for a, b in zip('A' + seq[:-1], seq)
                ) for seq in seqs)
            for eKey, seqs in v.items()
        }
        for sKey, v in numpadMoveSeq.items()
    }

# part 1
res = 0
d = getFinalKeyPressDict(2)
for inst in instLines:
    numVal = int(inst[:-1])
    counter = 0
    for a, b in zip('A' + inst[:-1], inst):
        counter += d[a][b]
    res += numVal * counter
print(res)

# part 2
res = 0
d = getFinalKeyPressDict(25)
for inst in instLines:
    numVal = int(inst[:-1])
    counter = 0
    for a, b in zip('A' + inst[:-1], inst):
        counter += d[a][b]
    res += numVal * counter
print(res)

