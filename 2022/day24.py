import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = """#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#"""

# inp = util.getInput(d=24, y=2022)

board = inp.splitlines()
dim = (len(board), len(board[0]))
innerDim = (len(board) - 2, len(board[0]) - 2)
initLoc = (0, board[0].index('.'))
goalLoc = (len(board) - 1, board[-1].index('.'))
currBliz = set()
blizDir = {
    '>': (0, 1),
    '<': (0, -1),
    'v': (1, 0),
    '^': (-1, 0),
}
moveDir = tuple(blizDir.values()) + ((0, 0),)

for i in range(dim[0]):
    for j in range(dim[1]):
        if board[i][j] in '<^v>':
            currBliz.add((i, j, board[i][j]))
locSet = set()
# loc i, loc j, reached goal 1, reached start 1, reached goal 2
locSet.add(initLoc + (False,) * 3)
t = 0
part1Answered = False
while True:
    if not part1Answered and goalLoc + (True, False, False) in locSet:
        print("part 1", t)
        part1Answered = True
    if goalLoc + (True,) * 3 in locSet:
        break
    t += 1
    # bliz move
    currBliz = set(tuple((b[i] + blizDir[b[2]][i] - 1) % innerDim[i] + 1
                         for i in range(2)) + (b[2],)
                   for b in currBliz)
    currBlizLoc = set(b[:-1] for b in currBliz)
    # player move
    newLocSet = set()
    for l in locSet:
        for d in moveDir:
            newPt = tuple(l[i] + d[i] for i in range(2))
            if all(0 <= newPt[i] < dim[i] for i in range(2)) \
                    and board[newPt[0]][newPt[1]] != '#' \
                    and newPt not in currBlizLoc:
                reachState = list(l[2:])
                if newPt == goalLoc:
                    if not reachState[0]:
                        reachState[0] = True
                    elif reachState[1]:
                        reachState[2] = True
                elif newPt == initLoc and reachState[0]:
                    reachState[1] = True
                newLocSet.add(newPt + tuple(reachState))
    locSet = newLocSet
print(t)


