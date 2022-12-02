import AOCInit
import util

inp = util.getInput(d=2, y=2015)
arr = list(list(int(c) for c in l.split('x')) for l in inp.splitlines())

def paperSize(side):
    p = util.prod(side)
    m = max(side)
    return p / m + sum(p / s for s in side) * 2

def ribbonSize(side):
    s = sum(side)
    m = max(side)
    return 2 * (s - m) + util.prod(side)

# part 1
print(sum(paperSize(l) for l in arr))

# part 2
print(sum(ribbonSize(l) for l in arr))

