import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=11, y=2022)

monkeyDesc = tuple(l.strip().split('\n') for l in inp.split('\n\n'))
monkeyCount = len(monkeyDesc)
monkeyOp = tuple((lambda oldVal, s=m[2].split(' = ')[1]: eval(s, dict(), {'old': oldVal}))
                 for m in monkeyDesc)
monkeyDivisor = tuple(util.getInts(m[3])[0] for m in monkeyDesc)
lcm = util.lcm(*monkeyDivisor)
monkeyTo = tuple(util.getInts(''.join(m[-2:]))[::-1] for m in monkeyDesc)

monkeyItems = list(list(util.getInts(m[1])) for m in monkeyDesc)
inspCount = [0] * monkeyCount

# part 1
for turn in range(20):
    for mIdx in range(monkeyCount):
        for item in monkeyItems[mIdx]:
            item = monkeyOp[mIdx](item) // 3
            monkeyItems[monkeyTo[mIdx][item % monkeyDivisor[mIdx] == 0]].append(item % lcm)
        inspCount[mIdx] += len(monkeyItems[mIdx])
        monkeyItems[mIdx] = list()
print(util.prod(sorted(inspCount, reverse=True)[:2]))

# part 2
monkeyItems = list(list(util.getInts(m[1])) for m in monkeyDesc)
inspCount = [0] * monkeyCount
for turn in range(10000):
    for mIdx in range(monkeyCount):
        for item in monkeyItems[mIdx]:
            item = monkeyOp[mIdx](item)
            monkeyItems[monkeyTo[mIdx][item % monkeyDivisor[mIdx] == 0]].append(item % lcm)
        inspCount[mIdx] += len(monkeyItems[mIdx])
        monkeyItems[mIdx] = list()
print(util.prod(sorted(inspCount, reverse=True)[:2]))

