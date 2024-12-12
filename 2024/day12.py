import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=12, y=2024)

garden = inp.splitlines()
n = len(garden)
m = len(garden[0])

geo = util.gridCompGeometry(garden)

# part 1
print(sum(bg.area * bg.perimeter for _, bg in geo))

# part 2
print(sum(bg.area * bg.countEdge for _, bg in geo))

