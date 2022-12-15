import AOCInit
import util
from collections import deque

if __name__ != '__main__':
    exit()

inp = tuple(l.split() for l in util.getInput(d=10, y=2016).splitlines())
rInst = dict()
rHold = dict()

# part 1
for inst in inp:
    if inst[0] == 'value':
        if inst[5] not in rHold:
            rHold[inst[5]] = list()
        rHold[inst[5]].append(int(inst[1]))
    else:
        (lowBot, highBot) = (('' if inst[5] == 'bot' else 'o') + inst[6],
                             ('' if inst[10] == 'bot' else 'o') + inst[11])
        for b in (lowBot, highBot):
            if b[0] == 'o' or b not in rHold:
                rHold[b] = list()
        rInst[inst[1]] = (lowBot, highBot)
botsToAct = deque(b for b in rInst.keys() if len(rHold[b]) == 2)
comparerBots = list()
while len(botsToAct) != 0:
    bot = botsToAct.popleft()
    (minC, maxC) = sorted(rHold[bot])
    if (minC, maxC) == (17, 61):
        comparerBots.append(bot)
    rHold[bot].clear()
    rHold[rInst[bot][0]].append(minC)
    rHold[rInst[bot][1]].append(maxC)
    botsToAct.extend(b for b in rInst[bot] if len(rHold[b]) == 2 and b[0] != 'o')
print(comparerBots)

# part 2
print(util.prod(util.flatten(rHold['o' + str(o)] for o in range(3))))

