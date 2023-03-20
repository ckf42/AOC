import AOCInit
import util
import typing as tp

if __name__ != '__main__':
    exit()

inp = util.getInput(d=3, y=2019)

wirePath = tuple(tuple((p[0], int(p[1:])) for p in l.split(','))
                 for l in inp.strip().splitlines())
dirList = {
    'R': util.Point(1, 0),
    'L': util.Point(-1, 0),
    'U': util.Point(0, 1),
    'D': util.Point(0, -1)
}

pathPts: tuple[list[util.Point], list[util.Point]] = (list(), list())
stepCounts: tuple[list[int], list[int]] = ([0], [0])
for i in (0, 1):
    currPt = util.MutPoint(0, 0)
    pathPts[i].append(currPt.asPoint())
    for (d, dist) in wirePath[i]:
        currPt += dist * dirList[d]
        pathPts[i].append(currPt.asPoint())
        stepCounts[i].append(stepCounts[i][-1] + dist)

# part 1
nearestDist: tp.Optional[int] = None
shortestDist: tp.Optional[int] = None
for i in range(len(wirePath[0])):
    for j in range(len(wirePath[1])):
        if (i, j) == (0, 0):
            continue
        insDist: tp.Optional[int] = None
        stepDist: tp.Optional[int] = None
        # check if segments intersect
        z = pathPts[1][j] - pathPts[0][i]
        d = dirList[wirePath[0][i][0]]
        e = dirList[wirePath[1][j][0]]
        det = d[1] * e[0] - d[0] * e[1]
        if det == 0:
            # parallel
            sIdx = 0 if d[0] == 0 else 1
            if z[sIdx] == 0:
                # same axis
                itvLst: list[list[int]] = sorted((
                        sorted((pathPts[k][l][1 - sIdx], pathPts[k][l + 1][1 - sIdx]))
                        for k, l in zip((0, 1), (i, j))))
                if itvLst[0][1] >= itvLst[1][0]:
                    insDist = abs(pathPts[0][i][sIdx]) \
                            + (0
                               if itvLst[0][1] * itvLst[1][0] <= 0
                               else min(map(abs, (itvLst[0][1], itvLst[1][0]))))
                    stepDist = abs(pathPts[0][i][1 - sIdx] - pathPts[1][j][1 - sIdx]) \
                            + stepCounts[0][i] + stepCounts[1][j]
        else:
            a = (z[1] * e[0] - z[0] * e[1]) // det
            b = (z[1] * d[0] - z[0] * d[1]) // det
            if all(0 <= c <= r
                   for (c, r) in zip((a, b),
                                     (wirePath[0][i][1], wirePath[1][j][1]))):
                insDist = (pathPts[0][i] + a * dirList[wirePath[0][i][0]]).norm(1)
                stepDist = a + b + stepCounts[0][i] + stepCounts[1][j]
        if nearestDist is None or (insDist is not None and insDist < nearestDist):
            nearestDist = insDist
        if shortestDist is None or (stepDist is not None and stepDist < shortestDist):
            shortestDist = stepDist
print(nearestDist)

# part 2
print(shortestDist)


