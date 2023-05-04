import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=11, y=2021)

initEnergyLevel = tuple(tuple(map(int, line))
                        for line in inp.splitlines())
dim = util.Point(len(initEnergyLevel), len(initEnergyLevel[0]))
energyLevel = {
    util.Point(i, j): initEnergyLevel[i][j]
    for i in range(dim[0])
    for j in range(dim[1])
}
directions = tuple(map(util.Point.fromIterable,
                       util.integerLattice(2, 1, p=util.inf)))


flashCount = 0
toFlash = list()
flashed = set()
turn = 0
while True:
    toFlash.clear()
    flashed.clear()
    for i in range(dim[0]):
        for j in range(dim[1]):
            pt = util.Point(i, j)
            energyLevel[pt] += 1
            if energyLevel[pt] > 9:
                toFlash.append(pt)
    while len(toFlash) != 0:
        pt = toFlash.pop()
        if pt in flashed:
            continue
        flashed.add(pt)
        for d in directions:
            newPt = pt + d
            if 0 <= newPt < dim:
                energyLevel[newPt] += 1
                if energyLevel[newPt] > 9:
                    toFlash.append(newPt)
    flashCount += len(flashed)
    for pt in flashed:
        energyLevel[pt] = 0
    if turn == 100 - 1:
        print(flashCount)
    if len(flashed) == len(energyLevel):
        print(turn + 1)
        break
    turn += 1

