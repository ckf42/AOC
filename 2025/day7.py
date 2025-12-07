import AOCInit
import util

if __name__ != '__main__':
    exit()


inp = util.getInput(d=7, y=2025)

grid, n, m = util.asGrid(inp)
x, y = divmod(inp.index('S'), m + 1)


fronts = {y: 1}
splitCount = 0
while x < n - 1:
    newFronts = dict()
    for y, count in fronts.items():
        if grid[x + 1][y] == '^':
            newFronts[y - 1] = newFronts.get(y - 1, 0) + count
            newFronts[y + 1] = newFronts.get(y + 1, 0) + count
            splitCount += 1
        else:
            newFronts[y] = newFronts.get(y, 0) + count
    fronts = newFronts
    x += 1
# part 1
print(splitCount)
# part 2
print(sum(fronts.values()))


