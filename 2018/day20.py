import AOCInit
import util
from collections import defaultdict

if __name__ != '__main__':
    exit()

inp = util.getInput(d=20, y=2018).strip()

# symbol: mask offset, move direction
dirDict = {
    'N': (3, 1j),
    'E': (2, 1),
    'S': (1, -1j),
    'W': (0, -1),
}
maskToDir = (-1, -1j, 1, 1j)
pathDict: defaultdict[complex, int] = defaultdict(int)

# ptr in str, location
stack: list[tuple[int, complex]] = list()
stack.append((1, 0))
while len(stack) != 0:
    (ptr, loc) = stack.pop()
    while inp[ptr] in 'NEWS':
        (offset, moveDir) = dirDict[inp[ptr]]
        pathDict[loc] |= (1 << offset)
        loc += moveDir
        ptr += 1
    if inp[ptr] == '$':
        break
    elif inp[ptr] == '(':
        stack.extend(((ptr, loc), (ptr + 1, loc)))
    elif inp[ptr] == '|':
        (_, prevLoc) = stack[-1]
        stack.append((ptr + 1, prevLoc))
    elif inp[ptr] == ')':
        (_, prevLoc) = stack.pop()
        stack.append((ptr + 1, prevLoc))
assert len(stack) == 0

distDict: dict[complex, int] = dict()
currDist = -1
locPts: frozenset[complex] = frozenset((0,))
while len(locPts) != 0:
    currDist += 1
    for loc in locPts:
        if loc not in distDict:
            distDict[loc] = currDist
    locPts = frozenset(
            loc + maskToDir[d]
            for loc in locPts
            for d in range(4)
            if pathDict[loc] & (1 << d) != 0 \
                    and loc + maskToDir[d] not in distDict)

# part 1
print(max(distDict.values()))

# part 2
print(len(tuple(filter(lambda d: d >= 1000, distDict.values()))))

