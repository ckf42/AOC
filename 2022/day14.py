import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = tuple(util.getInts(l) for l in util.getInput(d=14, y=2022).splitlines())
rockPathList = tuple(util.splitIntoGp(n, 2) for n in inp)
blocked = set()
maxLevel = -float('Inf')
for r in rockPathList:
    for idx in range(len(r) - 1):
        d = 1 if r[idx][0] == r[idx + 1][0] else 0
        incAmount = util.sgn(r[idx + 1][d] - r[idx][d])
        for coor in util.inclusiveRange(r[idx][d], r[idx + 1][d], None):
            blocked.add(tuple((coor if i == d else r[idx][i]) for i in range(2)))
    maxLevel = max(maxLevel, r[idx][1], r[idx + 1][1])
sandStart = (500, 0)
floorLevel = 2 + maxLevel


def fallSandStopLoc(currLoc):
    x = currLoc[0]
    for y in range(currLoc[1], floorLevel - 1):
        xOffset = util.firstSuchThat((0, -1, 1), lambda o: (x + o, y + 1) not in blocked)[1]
        if xOffset is None:
            return (x, y)
        else:
            x += xOffset
    return (x, floorLevel - 1)


# part 1 and part 2
counter = 0
part1Answered = False
while sandStart not in blocked:
    settledLoc = fallSandStopLoc(sandStart)
    if not part1Answered and settledLoc[1] > maxLevel:
        # part 1
        print(counter)
        part1Answered = True
    blocked.add(settledLoc)
    counter += 1
# part 2
print(counter)

