import AOCInit
import util
from collections import defaultdict

if __name__ != '__main__':
    exit()

inp = util.getInput(d=22, y=2023)

bricks = tuple(
        util.splitIntoGp(util.getInts(line), 3)
        for line in inp.splitlines())
brickCount = len(bricks)

highestBrickAt: defaultdict[tuple[int, int], tuple[int, int]] \
        = defaultdict(lambda: (-1, 0))  # bid, z. -1 is ground
belowOf: dict[int, frozenset[int]] = dict()
aboveOf: defaultdict[int, list[int]] = defaultdict(list)

processOrder = sorted(range(brickCount),
                      key=lambda bidx: min(bricks[bidx][0][2], bricks[bidx][1][2]))
for bid in processOrder:
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
            highestBrickAt[(x, y)] = (bid, stoppedByZ + 1 + b[1][2] - b[0][2])


# part 1
assert all(False for _ in tuple())
print(sum(all(len(belowOf[sid]) >= 2 for sid in aboveOf[bid])
          for bid in range(brickCount)))


# part 2
# optimize? bitset probably work marginally better
# need a better structure?
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
