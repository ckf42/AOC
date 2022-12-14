import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = tuple(util.getInts(l) for l in util.getInput(d=14, y=2022).splitlines())
rockPathList = tuple(util.splitIntoGp(n, 2) for n in inp)
blocked = set()
maxLevel = -float('Inf')
for r in rockPathList:
    for idx in range(len(r) - 1):
        d = 1 if r[idx][0] == r[idx + 1][0] else 0
        incAmount = util.sgn(r[idx + 1][d] - r[idx][d])
        for coor in util.inclusiveRange(r[idx][d], r[idx + 1][d], None):
            blocked.add(tuple((coor if i == d else r[idx][i]) for i in range(2)))
    maxLevel = max(maxLevel, r[idx][1], r[idx + 1][1])
sandStart = (500, 0)
floorLevel = 2 + maxLevel

counter = 0
part1Answered = False
planned = set()
stack = list()
stack.append(sandStart)
while len(stack) != 0:
    n = stack.pop()
    if n[1] >= floorLevel or n in blocked:
        continue
    nodesToAdd = list()
    for i in (0, -1, 1):
        if (nn := (n[0] + i, n[1] + 1)) not in blocked and nn not in planned:
            nodesToAdd.append(nn)
            planned.add(nn)
    if len(nodesToAdd) != 0:
        stack.extend([n] + nodesToAdd[::-1])
    else:
        counter += 1
        blocked.add(n)
        if not part1Answered and n[1] >= maxLevel:
            print(counter)
            part1Answered = True
print(counter)

