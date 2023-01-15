import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=19, y=2017)

traceMap = inp.splitlines()
dim = util.Point(len(traceMap), len(traceMap[0]))
directions = (
    util.Point(0, 1),
    util.Point(1, 0),
    util.Point(0, -1),
    util.Point(-1, 0),
)

loc = util.Point(0, util.firstIdxSuchThat(traceMap[0], lambda c: c != ' '))
currDir = 1
collectedLetters = list()
stepCount = 1
while True:
    possibleNewPt = tuple(
            (newDir, newPt, newC)
            for newDir in ((currDir + r) % 4 for r in (0, 1, -1))
            if 0 <= (newPt := loc + directions[newDir]) < dim \
                    and (newC := traceMap[newPt[0]][newPt[1]]) != ' '
    )
    if len(possibleNewPt) == 0:
        break
    stepCount += 1
    (currDir, loc, c) = possibleNewPt[0]
    if c not in '|-+':
        collectedLetters.append(c)

# part 1
print(''.join(collectedLetters))

# part 2
print(stepCount)

