import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=19, y=2022)

blueprints = tuple(l.split(': ', maxsplit=1)[1].split('. ')
                   for l in inp.splitlines())
blueCount = len(blueprints)
blueprintDict = [dict() for _ in blueprints]
for i in range(blueCount):
    for l in blueprints[i]:
        ls = l.strip('.').split(' ', maxsplit=4)
        spec = ls[-1].split(' and ')
        blueprintDict[i][ls[1]] = {ss[1]: int(ss[0])
                                   for item in spec if (ss := item.split(' ', maxsplit=1))}
propName = ('ore', 'clay', 'obsidian', 'geode')
propNameIdx = {'ore': 0, 'clay': 1, 'obsidian': 2, 'geode': 3}
robotCosts = tuple({item: max(botCost.get(item, 0) for botCost in bp.values())
                    for item in propName}
                   for bp in blueprintDict)

# part 1

# state: (time remain,
#         ore, clay, obs, geo,
#         ore bot, clay bot, obs bot, geo bot,
#         just bought bot)
def getOptimal(bpIdx, timeLimit):
    bp = blueprintDict[bpIdx]
    maxCosts = robotCosts[bpIdx]
    stack = list()
    visited = set()
    stack.append((timeLimit,) + (0,) * 4 + (1, 0, 0, 0) + (True,))
    currentOptimal = 0
    while len(stack) != 0:
        st = stack.pop()
        if st in visited:
            continue
        visited.add(st)
        currentOptimal = max(currentOptimal, st[4])
        if st[0] == 0:
            continue
        # cannot win current optimal
        if currentOptimal >= st[4] + st[8] * st[0] + (st[0] - 1) * st[0] // 2:
            continue
        # do nothing
        stack.append((st[0] - 1,) + tuple(st[1 + i] + st[5 + i] for i in range(4)) + st[5:9] + (False,))
        for botType in range(4):
            # excessive in store (include gen faster than spend)
            if botType != 3 and (st[1 + botType] >= (maxCosts[propName[botType]] - st[5 + botType]) * st[0]):
                continue
            # did not buy bot but could afford this one (thanks, reddit discussion board)
            if botType != 3 \
                    and not st[9] \
                    and all(st[1 + j] - st[5 + j] >= bp[propName[botType]].get(propName[j], 0)
                            for j in range(4)):
                continue
            mSt = list(st)
            for j in range(4):
                mSt[1 + j] -= bp[propName[botType]].get(propName[j], 0)
            # could not afford
            if any(mSt[1 + j] < 0 for j in range(4)):
                continue
            mSt[0] -= 1
            for j in range(4):
                mSt[1 + j] += st[5 + j]
            mSt[5 + botType] += 1
            mSt[9] = True
            stack.append(tuple(mSt))
    return currentOptimal

print(sum(getOptimal(i, 24) * (i + 1) for i in range(blueCount)))

# part 2
print(util.prod(getOptimal(i, 32) for i in range(min(blueCount, 3))))

