import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=25, y=2017)

instBlocks = inp.split('\n\n')
# state: (0: (write, movement, newState), 1: (write, movement, newState))
instDict: dict[str, tuple[tuple[int, int, str], ...]] = dict()
initState = instBlocks[0].split()[3][:-1]
checksumStep = util.getInts(instBlocks[0])[0]
for stateInst in instBlocks[1:]:
    instLines = stateInst.splitlines()
    valOrder = (1, 5) if '0' in instLines[1] else (5, 1)
    instDict[instLines[0].rsplit(maxsplit=1)[-1][:-1]] = tuple(
        (int(instLines[lIdx + 1][-2]),
         1 if 'right' in instLines[lIdx + 2] else -1,
         instLines[lIdx + 3].rsplit(maxsplit=1)[-1][:-1])
        for lIdx in valOrder)

# part 1
nonzeroLoc = set()
currState = initState
ptr = 0
for _ in range(checksumStep):
    inst = instDict[currState][ptr in nonzeroLoc]
    if inst[0]:
        nonzeroLoc.add(ptr)
    else:
        nonzeroLoc.discard(ptr)
    ptr += inst[1]
    currState = inst[2]
print(len(nonzeroLoc))

# part 2
# no part 2

