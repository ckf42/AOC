import AOCInit
import util
from collections import deque, defaultdict

if __name__ != '__main__':
    exit()

inp = util.getInput(d=20, y=2023)

modLinks: defaultdict[str, tuple[str, ...]] = defaultdict(tuple)
modTypes = defaultdict(str)
for line in inp.splitlines():
    source, dests = line.split(' -> ')
    mType = ''
    if source[0] in '%&':
        mType = source[0]
        source = source[1:]
    modTypes[source] = mType
    modLinks[source] = tuple(dests.split(', '))

flipState = {m: False for m, t in modTypes.items() if t == '%'}
conjInputState: dict[str, dict[str, bool]] = dict()
for m, destLst in modLinks.items():
    for d in destLst:
        if d not in conjInputState:
            conjInputState[d] = dict()
        if modTypes[d] == '&':
            conjInputState[d][m] = False

# for part 2
loopBegins = modLinks['broadcaster']
lastConjs = tuple(m for m, destLst in modLinks.items() if 'rx' in destLst)
assert len(lastConjs) == 1
lastConj = lastConjs[0]
assert modTypes[lastConj] == '&'
loopEnds = frozenset(m for m, destLst in modLinks.items() if lastConj in destLst)
assert len(loopBegins) == len(loopEnds)
assert all(modTypes[m] == '&' for m in loopEnds)
hitTimes: dict[str, list[int]] = {m: list() for m in loopEnds}

totalCount = [0, 0]
# no need to implement state memo: no hit in 10000 btn presses
step = 0
while not all(len(h) >= 2 for h in hitTimes.values()):
    step += 1
    q = deque((('broadcaster', False, ''),))
    totalCount[0] += 1
    while len(q) != 0:
        m, isHigh, source = q.popleft()
        if isHigh and source in loopEnds:
            hitTimes[source].append(step)  # hit time
        match modTypes[m]:
            case '':
                # for+append seems faster than extend
                for d in modLinks[m]:
                    q.append((d, isHigh, m))
                totalCount[isHigh] += len(modLinks[m])
            case '%' if not isHigh:
                flipState[m] = not flipState[m]
                for d in modLinks[m]:
                    q.append((d, flipState[m], m))
                totalCount[flipState[m]] += len(modLinks[m])
            case '&':
                conjInputState[m][source] = isHigh
                toSend = not all(conjInputState[m].values())
                for d in modLinks[m]:
                    q.append((d, toSend, m))
                totalCount[toSend] += len(modLinks[m])
    if step == 1000:
        print(util.prod(totalCount))

# for real wtf
# may need more cycle analysis for a more concrete proof
# period seems to be ~4000 anyway, so ~8000 steps in total
print(util.lcm(*(h[1] - h[0] for h in hitTimes.values())))

