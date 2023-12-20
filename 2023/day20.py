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
conjInputState: defaultdict[str, dict[str, bool]] = defaultdict(dict)
for m, destLst in modLinks.items():
    for d in destLst:
        if modTypes[d] == '&':
            conjInputState[d][m] = False

# for part 2
loopBegins = modLinks['broadcaster']
lastConjs = tuple(m for m, destLst in modLinks.items() if 'rx' in destLst)
assert len(lastConjs) == 1
lastConj = lastConjs[0]
assert modTypes[lastConj] == '&'
loopEnds = tuple(m for m, destLst in modLinks.items() if lastConj in destLst)
assert all(modTypes[m] == '&' for m in loopEnds)
loopHistory: dict[str, list[tuple[int, bool]]] = {m: list() for m in loopEnds}

totalCount = [0, 0]
# no need to implement state memo: no hit in 10000 btn presses
step = 0
for step in range(1, 10000 + 1):
    q = deque([('broadcaster', False, '')])  # m, is high, source
    roundPulseCount = [1, 0]
    while len(q) != 0:
        m, isHigh, source = q.popleft()
        if source in loopEnds:
            loopHistory[source].append((step, isHigh))  # hit time, sig type
        match modTypes[m]:
            case '':
                for d in modLinks[m]:
                    q.append((d, isHigh, m))
                roundPulseCount[isHigh] += len(modLinks[m])
            case '%':
                if not isHigh:
                    flipState[m] = not flipState[m]
                    for d in modLinks[m]:
                        q.append((d, flipState[m], m))
                    roundPulseCount[flipState[m]] += len(modLinks[m])
            case '&':
                conjInputState[m][source] = isHigh
                toSend = not all(conjInputState[m].values())
                for d in modLinks[m]:
                    q.append((d, toSend, m))
                roundPulseCount[toSend] += len(modLinks[m])
    for i in range(2):
        totalCount[i] += roundPulseCount[i]
    if step == 1000:
        print(util.prod(totalCount))

# for real wtf
# assumed cycles have no tails
hitTime = {
        m: tuple(step for step, isHigh in rec if isHigh)
        for m, rec in loopHistory.items()}
assert all(len(h) >= 2 for h in hitTime.values())
print(util.lcm(*(h[1] - h[0] for h in hitTime.values())))

