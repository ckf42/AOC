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
moveDir = {
        v: k
        for k, v in moveSig.items()
}

numpadMap = """\
789
456
123
 0A
""".splitlines()
numpadEdges = {
        numpadMap[i][j]: {
            moveSig[(ni - i, nj - j)]: numpadMap[ni][nj]
            for ni, nj in util.nearby2DGridPts((i, j), (4, 3))
            if numpadMap[ni][nj] != ' '
        }
        for i in range(4)
        for j in range(3)
        if numpadMap[i][j] != ' '
}
numpadKeys = tuple(numpadEdges.keys())

controllerMap = """\
 ^A
<v>
""".splitlines()
controllerEdges = {
        controllerMap[i][j]: {
            moveSig[(ni - i, nj - j)]: controllerMap[ni][nj]
            for ni, nj in util.nearby2DGridPts((i, j), (2, 3))
            if controllerMap[ni][nj] != ' '
        }
        for i in range(2)
        for j in range(3)
        if controllerMap[i][j] != ' '
}
controllerKeys = tuple(controllerEdges.keys())

numpadMoveSeq = dict()
for startKey in numpadKeys:
    numpadMoveSeq[startKey] = defaultdict(list)
    h = [(0, "", startKey)]
    costDict = dict()
    while len(h) != 0:
        cost, seq, key = hq.heappop(h)
        if costDict.get(key, cost + 1) < cost:
            continue
        costDict[key] = cost
        numpadMoveSeq[startKey][key].append(seq + 'A')
        for move, nextKey in numpadEdges[key].items():
            hq.heappush(h, (
                cost + (10 if len(seq) == 0 or move != seq[-1] else 1),
                seq + move,
                nextKey
            ))

controllerMoveSeq = dict()
for startKey in controllerKeys:
    controllerMoveSeq[startKey] = defaultdict(list)
    h = [(0, "", startKey)]
    costDict = dict()
    while len(h) != 0:
        cost, seq, key = hq.heappop(h)
        if costDict.get(key, cost + 1) < cost:
            continue
        costDict[key] = cost
        controllerMoveSeq[startKey][key].append(seq + 'A')
        for move, nextKey in controllerEdges[key].items():
            hq.heappush(h, (
                cost + (10 if len(seq) == 0 or move != seq[-1] else 1),
                seq + move,
                nextKey
            ))

# part 1

controllerMoveLen = {
    sKey: {
        eKey: min(len(seq) for seq in seqs)
        for eKey, seqs in v.items()
    }
    for sKey, v in controllerMoveSeq.items()
}

controllerMoveLen = {
    sKey: {
        eKey: min(sum(controllerMoveLen[a][b] for a, b in zip('A' + seq[:-1], seq)) for seq in seqs)
        for eKey, seqs in v.items()
    }
    for sKey, v in controllerMoveSeq.items()
}

numpadMoveLen = {
    sKey: {
        eKey: min(sum(controllerMoveLen[a][b] for a, b in zip('A' + seq[:-1], seq)) for seq in seqs)
        for eKey, seqs in v.items()
    }
    for sKey, v in numpadMoveSeq.items()
}

res = 0
for inst in instLines:
    numVal = int(inst[:-1])
    counter = 0
    for a, b in zip('A' + inst[:-1], inst):
        counter += numpadMoveLen[a][b]
    res += numVal * counter
print(res)

# part 2

controllerMoveLen = {
    sKey: {
        eKey: min(len(seq) for seq in seqs)
        for eKey, seqs in v.items()
    }
    for sKey, v in controllerMoveSeq.items()
}

for _ in range(25 - 1):
    controllerMoveLen = {
        sKey: {
            eKey: min(sum(controllerMoveLen[a][b] for a, b in zip('A' + seq[:-1], seq)) for seq in seqs)
            for eKey, seqs in v.items()
        }
        for sKey, v in controllerMoveSeq.items()
    }

numpadMoveLen = {
    sKey: {
        eKey: min(sum(controllerMoveLen[a][b] for a, b in zip('A' + seq[:-1], seq)) for seq in seqs)
        for eKey, seqs in v.items()
    }
    for sKey, v in numpadMoveSeq.items()
}

res = 0
for inst in instLines:
    numVal = int(inst[:-1])
    counter = 0
    for a, b in zip('A' + inst[:-1], inst):
        counter += numpadMoveLen[a][b]
    res += numVal * counter
print(res)



