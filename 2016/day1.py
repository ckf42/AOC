import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=1, y=2016).strip().split(', ')

# part 1
loc = (0, 0)
visited = set()
visited.add(loc)
hqLoc = None
lookDirList = ((0, 1), (1, 0), (0, -1), (-1, 0)) # L <- -> R
currDir = 0
for inst in inp:
    currDir = (currDir + (1 if inst[0] == 'R' else -1)) % 4
    for _ in range(int(inst[1:])):
        loc = tuple(loc[i] + lookDirList[currDir][i] for i in range(2))
        if loc in visited and hqLoc is None:
            hqLoc = loc
        visited.add(loc)
print(sum(map(abs, loc)))

# part 2
print(sum(map(abs, hqLoc)))

