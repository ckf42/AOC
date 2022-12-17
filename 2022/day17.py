import AOCInit
import util
import numpy as np

# if __name__ != '__main__':
    # exit()

flow = util.getInput(d=17, y=2022).strip()
flow = util.sub('<>', (-1, 1), flow)
flowIdx = 0

wellWidth = 7
rocks = (
    np.ones((4, 1), dtype=bool),
    np.reshape(np.array((0, 1, 0, 1, 1, 1, 0, 1, 0), dtype=bool), (3, 3)),
    np.rot90(np.reshape(np.array((0, 0, 1, 0, 0, 1, 1, 1, 1), dtype=bool), (3, 3)), k=-1),
    np.ones((1, 4), dtype=bool),
    np.ones((2, 2), dtype=bool)
)
rockShapes = tuple(r.shape for r in rocks)
rockIdx = 0
well = np.zeros((wellWidth, 10), dtype=bool)
extraSpace = np.zeros((wellWidth, 7), dtype=bool)

# def printWell():
    # for i in range(well.shape[1] - 1, -1, -1):
        # print('|', end='')
        # for j in range(wellWidth):
            # print(util.consoleChar(well[j, i]), end='')
        # print('|')
    # print('----------')

# def printRock(rIdx):
    # print('rock')
    # for i in range(rockShapes[rIdx][1] - 1, -1, -1):
        # for j in range(rockShapes[rIdx][0]):
            # print(util.consoleChar(rocks[rIdx][j, i]), end='')
        # print('')
    # print('----------')


def isValidPosition(coor, rIdx):
    return all((0 <= coor[0],
                coor[0] + rockShapes[rIdx][0] <= wellWidth,
                coor[1] >= 0)) \
            and not np.any(np.logical_and(rocks[rIdx],
                                          well[coor[0]:coor[0] + rockShapes[rIdx][0],
                                               coor[1]:coor[1] + rockShapes[rIdx][1]]))

fallCount = 10000
realHeight = 0
height = 0
heightSeq = [0]
for i in range(fallCount):
    if realHeight + 6 >= well.shape[1]:
        well = np.hstack((well, extraSpace))
    coor = [2, realHeight + 3]
    while True:
        if isValidPosition((coor[0] + flow[flowIdx], coor[1]), rockIdx):
            coor[0] += flow[flowIdx]
        flowIdx = (flowIdx + 1) % len(flow)
        if isValidPosition((coor[0], coor[1] - 1), rockIdx):
            coor[1] -= 1
        else:
            break
    np.logical_or(rocks[rockIdx],
                  well[coor[0]:coor[0] + rockShapes[rockIdx][0],
                       coor[1]:coor[1] + rockShapes[rockIdx][1]],
                  out=well[coor[0]:coor[0] + rockShapes[rockIdx][0],
                           coor[1]:coor[1] + rockShapes[rockIdx][1]])
    if coor[1] + rockShapes[rockIdx][1] > realHeight:
        height += coor[1] + rockShapes[rockIdx][1] - realHeight
        realHeight = coor[1] + rockShapes[rockIdx][1]
    filledRowIdx = None
    for i in range(coor[1] + rockShapes[rockIdx][1] - 1, coor[1] - 1, -1):
        if np.all(well[:, filledRowIdx]):
            filledRowIdx = i
            break
    if filledRowIdx is not None:
        well = well[:, filledRowIdx + 1:]
        realHeight = 0
    rockIdx = (rockIdx + 1) % len(rocks)
    heightSeq.append(height)

# part 1
print(heightSeq[2022])

# part 2
heightDiff = tuple(map(lambda i: heightSeq[i + 1] - heightSeq[i], range(len(heightSeq) - 1)))
(period, irreg) = util.findSeqPeriod(heightDiff, lambda t: t % len(rocks) == 0)

goal = 1000000000000
(rep, remainder) = divmod(goal - irreg, period)
print(
    heightSeq[irreg] \
    + (heightSeq[irreg + period] - heightSeq[irreg]) * rep \
    + (heightSeq[irreg + remainder] - heightSeq[irreg])
)
