import AOCInit
import util

if __name__ != '__main__':
    exit()

# idea from @juanplopes (on github) and @RiemannIntegirl (on reddit)
# not proud of it
# the idea is:
# 1. we only care about valves with positive flow
# 2. we only care what the maximal flow is, given time and init loc (and not how)
# 3. for part 2, elf and elephant will open distinct valves, so suffices to generate min time
#        for all possible final configurations (and combine them afterward)
#
# original idea is to use A* with wasted pressure as cost
# does not work well with part 2 as the combined search space is too large
# (killed after ~10 min and 3GM RAM with 8.6M nodes in heap)

inp = util.getInput(d=16, y=2022).splitlines()
allValveList = list([ls[1], util.getInts(ls[4])[0], tuple(v.strip(',') for v in ls[9:])]
                    for l in inp
                    if (ls := l.split()))
allValveCount = len(allValveList)
nodeNameDict = {allValveList[i][0]: i for i in range(allValveCount)}
for i in range(allValveCount):
    allValveList[i][2] = tuple(map(lambda n: nodeNameDict[n],
                                   allValveList[i][2]))
positiveValves = tuple(filter(lambda i: allValveList[i][1] > 0,
                              range(allValveCount)))
positiveCount = len(positiveValves)
positiveIdxDict = {positiveValves[i]: i for i in range(positiveCount)}
allPositiveNei = tuple(tuple(filter(lambda n: n in positiveValves, v[2]))
                       for v in allValveList)
dist = util.allPairDistances(range(allValveCount),
                             lambda i, j: 1 if j in allValveList[i][2] else None)
positiveFlows = tuple(allValveList[i][1] for i in positiveValves)

def getOptimalTrip(timeRemain):
    optimalRes = dict()
    stack = list() # (remain time, current loc, current flows, visit status)
    stack.append((timeRemain, nodeNameDict['AA'], 0) + (False,) * positiveCount)
    while len(stack) != 0:
        st = stack.pop()
        # (wait till) time's up
        optimalRes[st[3:]] = max(optimalRes.get(st[3:], 0), st[2])
        for n in positiveValves:
            # transfer
            cost = dist[(st[1], n)] + 1
            pid = positiveIdxDict[n]
            if not st[3 + pid] and st[0] > cost:
                stack.append((st[0] - cost, n, st[2] + positiveFlows[pid] * (st[0] - cost)) \
                            + tuple((True if i == pid else st[3 + i])
                                    for i in range(positiveCount)))
    return optimalRes

# part 1
print(max(getOptimalTrip(30).values()))

# part 2
resDict = getOptimalTrip(26)
k = tuple(resDict.keys())
print(max(resDict[k[i]] + resDict[k[j]]
          for i in range(len(k) - 1)
          for j in range(i + 1, len(k))
          if not any(k[i][l] and k[j][l] for l in range(positiveCount))))

