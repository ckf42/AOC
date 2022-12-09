import AOCInit
import util
import heapq as hq

if __name__ != '__main__':
    exit()

inp = util.getInput(d=14, y=2015).splitlines()
timeElasp = 2503
deerDict = {name: util.getInts(l)
            for l in inp
            if (name := l.split(maxsplit=1)[0])}
deerCount = len(deerDict)

# part 1
def dist(s):
    d, m = divmod(timeElasp, s[1] + s[2])
    return (d * s[1] + min(m, s[1])) * s[0]

deerDist = tuple((name, dist(deerDict[name]))
                 for name in deerDict.keys())
print(max(deerDist, key=lambda t: t[1])[1])

# part 2
deerPlace = list()
deerStatus = dict()

def increPt(idx):
    if idx < deerCount and deerPlace[0][0] == deerPlace[idx][0]:
        deerStatus[deerPlace[idx][1]][2] += 1
        increPt(idx * 2 + 1)
        increPt(idx * 2 + 2)

for deer, status in deerDict.items():
    # 0: neg dist, 1: name
    hq.heappush(deerPlace, [0, deer])
    # 0: isResting, 1: timeTillStateChange, 2: score
    deerStatus[deer] = [False, status[1], 0]
for _ in range(timeElasp):
    for dIdx in range(deerCount):
        # progress state
        deerName = deerPlace[dIdx][1]
        isResting = deerStatus[deerName][0]
        if not isResting:
            deerPlace[dIdx][0] -= deerDict[deerName][0] # hq is min heap
        deerStatus[deerName][1] -= 1
        if deerStatus[deerName][1] == 0:
            # change state
            deerStatus[deerName][0] = not isResting
            deerStatus[deerName][1] = deerDict[deerName][1 if isResting else 2]
    hq.heapify(deerPlace)
    increPt(0)
print(max(s[2] for s in deerStatus.values()))

