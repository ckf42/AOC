import AOCInit
import util

if __name__ != '__main__':
    exit()

# TODO: go with u/askalski's algorithm

inp = util.getInput(d=16, y=2016).strip()
initLen = len(inp)
initState = list(c == '1' for c in inp)
revNegInitState = list(not c for c in initState[::-1])

segJoiner = [False]

def ensureJoinerLen(l):
    while len(segJoiner) < l:
        segJoiner.extend([False] + [not c for c in segJoiner[::-1]])

def getChecksum(targetLen):
    ensureJoinerLen((targetLen + 1) // (initLen + 1))
    chunkSize = targetLen & -targetLen
    checkSumStream = list()
    remainParts = list()
    joinerIdx = 0
    useOgInp = True
    for _ in range(targetLen // chunkSize):
        while len(remainParts) < chunkSize:
            remainParts += (initState if useOgInp else revNegInitState) \
                    + segJoiner[joinerIdx:joinerIdx + 1]
            joinerIdx += 1
            useOgInp = not useOgInp
        checkSumStream.append(sum(remainParts[:chunkSize]) & 1 == 0)
        remainParts = remainParts[chunkSize:]
    return ''.join(util.sub((True, False), '10', checkSumStream))


# part 1
print(getChecksum(272))

# part 2
print(getChecksum(35651584))


