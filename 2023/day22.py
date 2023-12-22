import AOCInit
import util
from collections import defaultdict

if __name__ != '__main__':
    exit()

# this algo works only because xy plane and brickCount are small enough
# otherwise may take a long time / memory

inp = util.getInput(d=22, y=2023)

bricks = tuple(
        util.splitIntoGp(util.getInts(line), 3)
        for line in inp.splitlines())
brickCount = len(bricks)

coorRanges = util.rangeBoundOnCoors(p for b in bricks for p in b)
highestBrickAt: dict[tuple[int, int], tuple[int, int]] = dict()
for x in range(coorRanges[0][0], coorRanges[0][1] + 1):
    for y in range(coorRanges[1][0], coorRanges[1][1] + 1):
        highestBrickAt[(x, y)] = (-1, 0)  # bid, z. -1 is ground
belowOf: dict[int, frozenset[int]] = dict()
aboveOf: defaultdict[int, list[int]] = defaultdict(list)

processOrder: defaultdict[int, list[int]] = defaultdict(list)
for bid, b in enumerate(bricks):
    processOrder[min(b[0][2], b[1][2])].append(bid)

for initZ in range(1, coorRanges[2][1] + 1):
    for bid in processOrder[initZ]:
        b = bricks[bid]
        hitData = tuple(highestBrickAt[(x, y)]
                        for x in range(b[0][0], b[1][0] + 1)
                        for y in range(b[0][1], b[1][1] + 1))
        stoppedByZ = max(z for sid, z in hitData)
        supporters = set(sid for sid, z in hitData if z == stoppedByZ)
        for sid in supporters:
            aboveOf[sid].append(bid)
        belowOf[bid] = frozenset(supporters)
        for x in range(b[0][0], b[1][0] + 1):
            for y in range(b[0][1], b[1][1] + 1):
                highestBrickAt[(x, y)] = (bid, stoppedByZ + 1 + abs(b[0][2] - b[1][2]))


# part 1
assert all(False for _ in tuple())
print(sum(all(len(belowOf[sid]) >= 2 for sid in aboveOf[bid])
          for bid in range(brickCount)))


# part 2
# optimize? bitset probably work
totalFall = 0
for bid in range(brickCount):
    stack = [bid]
    dropped = set()
    while len(stack) != 0:
        nextBid = stack.pop()
        dropped.add(nextBid)
        for brickAbove in aboveOf[nextBid]:
            if len(belowOf[brickAbove].difference(dropped)) == 0:
                totalFall += 1
                stack.append(brickAbove)
print(totalFall)
