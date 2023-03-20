import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=12, y=2019)

pos: list[util.MutPoint] = list(util.MutPoint(*util.getInts(l))
                                for l in inp.splitlines())
vel: list[util.MutPoint] = list(util.MutPoint.zero(3) for _ in range(4))

# part 1
simuTime = 1000
for _ in range(simuTime):
    # gravity
    for i in range(4 - 1):
        for j in range(i, 4):
            diff = pos[i] - pos[j]
            f = util.Point(*(util.sgn(diff[d]) for d in range(3)))
            vel[i] -= f
            vel[j] += f
    # apply vel
    for i in range(4):
        pos[i] += vel[i]
print(sum(pos[i].norm(1) * vel[i].norm(1) for i in range(4)))

# part 2
# ~16s with total simu ~615k steps
pos = list(util.MutPoint(*util.getInts(l)) for l in inp.splitlines())
periods = list()
for d in range(3):
    coorPos = util.MutPoint(*(pos[i][d] for i in range(4)))
    coorVel = util.MutPoint.zero(4)
    currTime: int = 0
    stateList: dict[tuple[util.Point, util.Point], int] = {}
    while (st := (coorPos.asPoint(), coorVel.asPoint())) not in stateList:
        stateList[st] = currTime
        for i in range(4 - 1):
            for j in range(i + 1, 4):
                coorF = util.sgn(coorPos[i] - coorPos[j])
                coorVel[i] -= coorF
                coorVel[j] += coorF
        coorPos += coorVel
        currTime += 1
    periods.append(currTime - stateList[st])
print(util.lcm(*periods))
