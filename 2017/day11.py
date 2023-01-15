import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=11, y=2017)

dirInst = inp.strip().split(',')
# a / 2 + b * i sqrt(3) / 2
coorDict = {k: util.Point.fromIterable(v) for k, v in
    {
        'n': (2, 0),
        's': (-2, 0),
        'ne': (1, 1),
        'se': (-1, 1),
        'nw': (1, -1),
        'sw': (-1,-1),
    }.items()
}

loc = util.Point(0, 0)
maxDist = 0
for inst in dirInst:
    loc = loc + coorDict[inst]
    maxDist = max(maxDist, loc.norm(1) // 2)

# part 1
print(loc.norm(1) // 2)

# part 2
print(maxDist)

