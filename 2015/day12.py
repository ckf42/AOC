import AOCInit
import util
import re
import bisect

if __name__ != '__main__':
    exit()

inp = util.getInput(d=12, y=2015).strip()

# part 1
print(sum(util.getInts(inp)))

# part 2
bIndices = list((s, 1 if inp[s] == '{' else -1) for m in re.finditer('{|}', inp) if (s := m.start()))
bIndices.sort(key=lambda x: x[0])
(bIndices, bValue) = util.multiMap(bIndices, (lambda x: x[0], lambda x: x[1]))
l = len(bIndices)
vIndices = tuple(m.start() for m in re.finditer(':"red"', inp))
inpList = list(inp)

def findBraces(idx):
    bIdx = bisect.bisect(bIndices, idx)
    leftIdx = util.firstAccumSuchThat(bValue[bIdx - 1:0:-1],
                                      lambda x, y: x + y,
                                      lambda z: z > 0)[0]
    rightIdx = util.firstAccumSuchThat(bValue[bIdx:l],
                                       lambda x, y: x + y,
                                       lambda z: z < 0)[0]
    return (bIndices[bIdx - 1 - leftIdx], bIndices[rightIdx + bIdx])

for idx in vIndices:
    if inpList[idx] != 'x':
        p = findBraces(idx)
        inpList[p[0]:p[1]] = ['x'] * (p[1] - p[0])
print(sum(util.getInts(''.join(inpList))))

