import AOCInit
import util
import intCode as ic

if __name__ != '__main__':
    exit()

inp = util.getInput(d=11, y=2019)

code = util.getInts(inp)
directions = tuple(map(lambda c: complex(*c),
                       ((1, 0), (0, 1), (-1, 0), (0, -1))))

# part 1
currLoc: complex = 0
whitePanels: set[complex] = set()
painted: set[complex] = set()
currDir = 1
prog = ic.IntCode(code)
while prog.isRunning:
    prog.send(0 if currLoc not in whitePanels else 1)
    try:
        if prog.get() == 1:
            whitePanels.add(currLoc)
            painted.add(currLoc)
        else:
            whitePanels.discard(currLoc)
        currDir = (currDir + (-1 if prog.get() == 1 else 1)) % 4
    except StopIteration:
        break
    currLoc += directions[currDir]
print(len(painted))


# part 2
currLoc = 0
whitePanels.clear()
whitePanels.add(currLoc)
currDir = 1
prog = ic.IntCode(code)
while prog.isRunning:
    prog.send(0 if currLoc not in whitePanels else 1)
    try:
        if prog.get() == 1:
            whitePanels.add(currLoc)
        else:
            whitePanels.discard(currLoc)
        currDir = (currDir + (-1 if prog.get() == 1 else 1)) % 4
    except StopIteration:
        break
    currLoc += directions[currDir]
bounds = util.rangeBound(util.takeApart(tuple(map(util.complexToTuple, whitePanels))))
for j in util.inclusiveRange(*bounds[1])[::-1]:
    for i in util.inclusiveRange(*bounds[0]):
        print(util.consoleChar(complex(i, j) in whitePanels),
              end='')
    print('')
