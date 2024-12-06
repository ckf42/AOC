import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=6, y=2024)

labMap = inp.splitlines()
n = len(labMap)
m = len(labMap[0])
dirs: tuple[tuple[int, int], ...] = ((-1, 0), (0, 1), (1, 0), (0, -1))

obs = set(
        (i, j)
        for i in range(n)
        for j in range(m)
        if labMap[i][j] == '#'
)

# part 1
x, y = divmod(inp.index('^'), m + 1)
guardDir = 0
visited = set()
while 0 <= x < n and 0 <= y < m:
    visited.add((x, y))
    xx = x + dirs[guardDir][0]
    yy = y + dirs[guardDir][1]
    rightDir = (guardDir + 1) % 4
    if (xx, yy) in obs:
        guardDir = rightDir
    else:
        x, y = xx, yy
print(len(visited))

# part 2
def walkHasLoop(obsSet):
    x, y = divmod(inp.index('^'), m + 1)
    d = 0
    visitedState = set()
    while 0 <= x < n and 0 <= y < m:
        if (x, y, d) in visitedState:
            return True
        visitedState.add((x, y, d))
        xx = x + dirs[d][0]
        yy = y + dirs[d][1]
        rightDir = (d + 1) % 4
        if (xx, yy) in obsSet:
            d = rightDir
        else:
            x, y = xx, yy
    return False

path = tuple(pt for pt in visited if pt != divmod(inp.index('^'), m + 1))
print(sum(walkHasLoop(obs | {pt}) for pt in path))

