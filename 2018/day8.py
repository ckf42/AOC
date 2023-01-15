import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=8, y=2018)

licenseNumber = util.getInts(inp)
# id: (child id, metadata)
nodeDict: dict[int, tuple[tuple[int, ...], tuple[int, ...]]] = dict()

def getNodeEnd(nodeBeginPtr, lastUsedNodeIdx):
    # returns node end ptr, last used idx for child
    childCount = licenseNumber[nodeBeginPtr]
    metaLen = licenseNumber[nodeBeginPtr + 1]
    childIdxList = list()
    ptr = nodeBeginPtr + 2
    nIdx = lastUsedNodeIdx
    for _ in range(childCount):
        ptr, nIdx = getNodeEnd(ptr, nIdx)
        childIdxList.append(nIdx)
    nodeDict[nIdx + 1] = (tuple(childIdxList), tuple(licenseNumber[ptr:ptr + metaLen]))
    return (ptr + metaLen, nIdx + 1)

(_, rootIdx) = getNodeEnd(0, -1)

# part 1
print(sum(map(lambda n: sum(n[1]), nodeDict.values())))

# part 2
valueDict = dict()

def getValue(nodeIdx):
    if nodeIdx not in valueDict:
        n = nodeDict[nodeIdx]
        if len(n[0]) == 0:
            valueDict[nodeIdx] = sum(n[1])
        else:
            childSum = 0
            for idx in n[1]:
                if idx <= len(n[0]):
                    childSum += getValue(n[0][idx - 1])
            valueDict[nodeIdx] = childSum
    return valueDict[nodeIdx]

print(getValue(rootIdx))

