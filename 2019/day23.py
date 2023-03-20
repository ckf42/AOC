import AOCInit
import util
import intCode as ic

if __name__ != '__main__':
    exit()

inp = util.getInput(d=23, y=2019)
code = util.getInts(inp)
computers: list[ic.IntCode] = list(ic.IntCode(code, (i,)) for i in range(50))
packageQueues: list[list[int]] = list(list() for _ in range(50))
waitedTurns: list[int] = list(0 for _ in range(50))
part1Answered = False
currNatPackage = None
lastSentNatPackage = None
while True:
    for i in range(50):
        assert not computers[i].isHalted
        packages = util.splitIntoGp(computers[i].pump(), 3, allowRemain=False)
        for p in packages:
            if p[0] == 255:
                if not part1Answered:
                    print(p[2])
                    part1Answered = True
                currNatPackage = p[1:]
            else:
                packageQueues[p[0]].extend(p[1:])
        computers[i].purge()
    if all(len(q) == 0 for q in packageQueues) and all(t >= 2 for t in waitedTurns):
        # idle
        assert currNatPackage is not None
        if lastSentNatPackage is not None \
                and currNatPackage[1] == lastSentNatPackage[1]:
            print(currNatPackage[1])
            break
        computers[0].send(*currNatPackage)
        waitedTurns[0] = 0
        for i in range(1, 50):
            computers[i].send(-1)
            waitedTurns[i] = 0
        lastSentNatPackage = currNatPackage
    else:
        for i in range(50):
            if len(packageQueues[i]) == 0:
                computers[i].send(-1)
                waitedTurns[i] += 1
            else:
                computers[i].send(*packageQueues[i])
                packageQueues[i].clear()
                waitedTurns[i] = 0

