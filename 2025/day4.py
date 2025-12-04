import AOCInit
import util

if __name__ != "__main__":
    exit()

inp = util.getInput(d=4, y=2025)

grid = list(line.strip() for line in inp.splitlines())
n, m = len(grid), len(grid[0])
rollLocs = set((i, j) for i in range(n) for j in range(m) if grid[i][j] == "@")

# part 1
print(sum(1 for pt in rollLocs if sum(grid[x][y] == "@" for x, y in util.nearby2DGridPts(pt, (n, m), isL1=False)) < 4))


# part 2
total = 0
buff = rollLocs.copy()
while len(buff) != 0:
    newBuff = set()
    for pt in buff:
        if pt not in rollLocs:
            continue
        nbPts = [nb for nb in util.nearby2DGridPts(pt, isL1=False) if nb in rollLocs]
        if len(nbPts) < 4:
            total += 1
            rollLocs.remove((pt))
            newBuff.update(nbPts)
    buff = newBuff
print(total)
