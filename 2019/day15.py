import AOCInit
import util
import intCode as ic

if __name__ != '__main__':
    exit()

inp = util.getInput(d=15, y=2019)
code = util.getInts(inp)
directions = tuple(map(lambda t: complex(*t),
                       util.integerLattice(2, 1)))
dirToCmd: dict[complex, int] = {
    complex(0, 1): 1,
    complex(0, -1): 2,
    complex(-1, 0): 3,
    complex(1, 0): 4,
}
cmdToDir: dict[int, complex] = {v: k for k, v in dirToCmd.items()}

prog = ic.IntCode(code)
droidLoc: complex = complex(0, 0)
# loc: space type (0=wall, 1=space, 2=goal)
knownMap: dict[complex, int] = dict()
knownMap[droidLoc] = 1 # init always space
unknownBoundary: set[complex] = set(directions)

def pathToUnknown() -> tuple[complex, tuple[int, ...]]:
    """
    Return the nearest unknown block and seq of cmd to it
    """
    cmdToGetHere: dict[complex, int] = dict()
    h: util.Heap[tuple[int, complex]] = util.MinHeap(key=lambda pr: pr[0])
    visited: set[complex] = set()
    h.push((0, droidLoc))
    while not h.isEmpty():
        (cost, loc) = h.pop()
        if loc in visited:
            continue
        if loc in unknownBoundary:
            unknownLoc = loc
            cmdSeq: list[int] = list()
            while loc != droidLoc:
                cmd = cmdToGetHere[loc]
                cmdSeq.append(cmd)
                loc -= cmdToDir[cmd]
            return (unknownLoc, tuple(cmdSeq[::-1]))
        visited.add(loc)
        for d in directions:
            newLoc = loc + d
            if knownMap.get(newLoc, 1) != 0 and newLoc not in visited:
                h.push((cost + 1, newLoc))
                cmdToGetHere[newLoc] = dirToCmd[d]
    raise RuntimeError("Cannot find path to unknown block")

oxygenPt = None
while len(unknownBoundary) != 0:
    (newLoc, pathCmd) = pathToUnknown()
    prog.send(*pathCmd)
    prog.run(pauseOnOutput=False, pauseOnInput=True)
    assert prog.state != ic.IntCodeState.HALTED
    status = prog.outputBuffer[-1]
    prog.purge()
    knownMap[newLoc] = status
    unknownBoundary.remove(newLoc)
    if status == 0:
        droidLoc = newLoc - cmdToDir[pathCmd[-1]]
    else:
        if status == 2:
            oxygenPt = newLoc
        droidLoc = newLoc
        unknownBoundary.update(
                tuple(nei
                      for d in directions
                      if (nei := droidLoc + d) not in knownMap))
assert oxygenPt is not None

# bounds = util.rangeBound(util.takeApart(tuple(map(util.complexToTuple, knownMap.keys()))))
# for i in util.inclusiveRange(*bounds[0]):
    # for j in util.inclusiveRange(*bounds[1]):
        # c = ' '
        # pt = complex(i, j)
        # if pt == complex(0, 0):
            # c = 'o'
        # elif pt in knownMap:
            # ty = knownMap[pt]
            # if ty == 2:
                # c = 'x'
            # else:
                # c = util.consoleChar(ty == 0)
        # else:
            # c = util.consoleChar(None)
        # print(c, end='')
    # print('')

# part 1
print(util.dijkstra(initialNode=complex(0, 0),
                    costFunc=lambda nst, ost, oc: oc + 1,
                    neighbourListFunc=lambda pt: tuple(
                        ptd
                        for d in directions
                        if knownMap[(ptd := pt + d)] != 0),
                    goalCheckerFunc=lambda pt: pt == oxygenPt)[1])

# part 2
maxFillTime: int = 0
h: util.Heap[tuple[int, complex]] = util.MinHeap(key=lambda pr: pr[0])
h.push((0, oxygenPt))
filledPt: set[complex] = set()
while not h.isEmpty():
    (fillTime, pt) = h.pop()
    if pt in filledPt:
        continue
    filledPt.add(pt)
    maxFillTime = max(maxFillTime, fillTime)
    for d in directions:
        ptd = pt + d
        if ptd not in filledPt and knownMap[ptd] != 0:
            h.push((fillTime + 1, ptd))
print(maxFillTime)


