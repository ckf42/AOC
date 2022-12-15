import AOCInit
import util
import re

if __name__ != '__main__':
    exit()

inp = util.getInput(d=9, y=2016).strip()
markerRe = re.compile(r'\(\d+x\d+\)')

# part 1
def decompressedLen(inpStr, doRecursive=False):
    dLen = 0
    pidx = 0
    midx = 0
    markerList = tuple(markerRe.finditer(inpStr))
    while pidx < len(inpStr):
        midxOffset = util.firstIdxSuchThat(markerList[midx:], lambda m: m.start() >= pidx)
        if midxOffset is None:
            # no more compressed data
            dLen += len(inpStr) - pidx
            break
        midx += midxOffset
        (s, e) = (markerList[midx].start(), markerList[midx].end())
        markerInfo = util.getInts(markerList[midx].group())
        dLen += s - pidx \
                + markerInfo[1] * (decompressedLen(inpStr[e:e + markerInfo[0]], True)
                                   if doRecursive
                                   else markerInfo[0])
        pidx = e + markerInfo[0]
        midx += 1
    return dLen

print(decompressedLen(inp, False))

# part 2
print(decompressedLen(inp, True))

