import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = """....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#.."""
inp = util.getInput(d=23, y=2022)

board = inp.splitlines()
elfLoc = set()
for i in range(len(board)):
    for j in range(len(board[i])):
        if board[i][j] == '#':
            elfLoc.add((i, j))

directions = (
    ((-1, 0), (-1, -1), (-1, 1)), # N
    ((1, 0), (1, -1), (1, 1)), # S
    ((0, -1), (1, -1), (-1, -1)), # W
    ((0, 1), (1, 1), (-1, 1)), # E
)
surrDir = set(util.flatten(directions))

def printElf():
    elfRange = util.multiMap(util.transpose(tuple(elfLoc)), (min, max))
    for i in util.inclusiveRange(elfRange[0][0], elfRange[1][0]):
        for j in util.inclusiveRange(elfRange[0][1], elfRange[1][1]):
            print(util.consoleChar((i, j) in elfLoc), end='')
        print('')
    print('-----')

# part 1
turnCount = 0
while True:
    hasMoved = False
    # consider
    proposedLocReg = dict() # proposed loc: list(original loc)
    for elf in elfLoc:
        if any(tuple(elf[i] + d[i] for i in range(2)) in elfLoc
               for d in surrDir):
            proposedLoc = None
            for offset in range(4):
                dirToCheck = directions[(turnCount + offset) % 4]
                if not any(tuple(elf[i] + d[i] for i in range(2)) in elfLoc
                        for d in dirToCheck):
                    proposedLoc = tuple(elf[i] + dirToCheck[0][i] for i in range(2))
                    break
            if proposedLoc is not None:
                if proposedLoc not in proposedLocReg:
                    proposedLocReg[proposedLoc] = list()
                proposedLocReg[proposedLoc].append(elf)
    # move
    for targetLoc, proposingElves in proposedLocReg.items():
        if len(proposingElves) == 1:
            elfLoc.remove(proposingElves[0])
            elfLoc.add(targetLoc)
            hasMoved = hasMoved or targetLoc != proposingElves[0]
    if not hasMoved:
        break
    turnCount += 1
    if turnCount == 10:
        elfRange = util.multiMap(util.transpose(tuple(elfLoc)), (min, max))
        print(util.prod(1 + elfRange[1][i] - elfRange[0][i] for i in range(2)) - len(elfLoc))

# part 2
print(turnCount + 1)

