import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=6, y=2024)

labMap = inp.splitlines()
n = len(labMap)
m = len(labMap[0])
dirs: tuple[tuple[int, int], ...] = ((-1, 0), (0, 1), (1, 0), (0, -1))

obs = [
    [labMap[i][j] == '#' for j in range(m)]
    for i in range(n)
]

# part 1
x0, y0 = divmod(inp.index('^'), m + 1)
x, y = x0, y0
guardDir = 0
visited = set()
while 0 <= x < n and 0 <= y < m:
    visited.add((x, y))
    xx = x + dirs[guardDir][0]
    yy = y + dirs[guardDir][1]
    rightDir = (guardDir + 1) % 4
    if 0 <= xx < n and 0 <= yy < m and obs[xx][yy]:
        guardDir = rightDir
    else:
        x, y = xx, yy
print(len(visited))

# part 2
def walkHasLoop():
    x, y = x0, y0
    d = 0
    visitedState = set()
    while 0 <= x < n and 0 <= y < m:
        if (x, y, d) in visitedState:
            return True
        visitedState.add((x, y, d))
        xx = x + dirs[d][0]
        yy = y + dirs[d][1]
        rightDir = (d + 1) % 4
        if 0 <= xx < n and 0 <= yy < m and obs[xx][yy]:
            d = rightDir
        else:
            x, y = xx, yy
    return False

counter = 0
for pt in visited:
    if pt == (x0, y0):
        continue
    obs[pt[0]][pt[1]] = True
    counter += walkHasLoop()
    obs[pt[0]][pt[1]] = False
print(counter)

