import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=24, y=2017)

edges = tuple(map(util.getInts, inp.splitlines()))
edgeSums = tuple(map(sum, edges))
edgeCount = len(edges)
edgeList = {
    node: frozenset(filter(lambda idx: node in edges[idx], range(edgeCount)))
    for node in frozenset(util.flatten(edges))
}

# part 1
# (usedEdge, currLoc, strength, len)
visitedStates: set[tuple[int, int, int, int]] = set()
maxStrength = 0
maxLenStrength = (0, 0) # len, strength
stack = list()
stack.append((0, 0, 0, 0))
while len(stack) != 0:
    (used, currLoc, strength, currLen) = stack.pop()
    if (used, currLoc, strength, currLen) in visitedStates:
        continue
    visitedStates.add((used, currLoc, strength, currLen))
    maxStrength = max(maxStrength, strength)
    if maxLenStrength[0] < currLen \
            or (maxLenStrength[0] == currLen and maxLenStrength[1] < strength):
        maxLenStrength = (currLen, strength)
    for eIdx in edgeList[currLoc]:
        msk = 1 << eIdx
        if used & msk == 0:
            stack.append((used | msk,
                          edgeSums[eIdx] - currLoc,
                          strength + edgeSums[eIdx],
                          currLen + 1))
print(maxStrength)

# part 2
print(maxLenStrength[1])


