import AOCInit
import util
from statistics import median
from collections import defaultdict

if __name__ != '__main__':
    exit()

inp = util.getInput(d=7, y=2021)

crabPos = util.getInts(inp)

# part 1
med = median(crabPos)
print(int(sum(abs(pos - med) for pos in crabPos)))

# part 2
# dist is sum((d^2 + d) / 2) with d = abs(pt - x)
# pt solves 2 (n * pt - s) = -sum(sgn(pt - x)) = count(x > pt) - count(x < pt) = r
# enumerate all possible r, check if pt is correct
# ~n ln n time, ~n space
s = sum(crabPos)
r = len(crabPos)
count: defaultdict[int, int] = defaultdict(int)
for pos in crabPos:
    count[pos] += 1
uqPos = sorted(count.keys())
minPt = None
for i, v in enumerate(uqPos[:-1]):
    # at v
    r -= count[v]
    pt = (r / 2 + s) / len(crabPos)
    if pt == v:
        minPt = v
        break
    # higher than v
    r -= count[v]
    pt = (r / 2 + s) / len(crabPos)
    if v < pt < uqPos[i + 1]:
        minPt = pt
        break
if minPt is None:
    # at last
    r -= count[uqPos[-1]]
    assert r == count[uqPos[-1]] - len(crabPos)
    pt = (r / 2 + s) / len(crabPos)
    if pt == uqPos[-1]:
        minPt = v
assert minPt is not None

def dist(p):
    return sum(d * (d + 1) / 2
               for x in crabPos
               if (d := abs(p - x)))

# deal with int pos
# TODO: use rounding instead?
pti = int(pt)
ptList: tuple[int, ...] = (pti,)
if pt != pti:
    ptList = (pti, pti + 1)
print(int(min(dist(x) for x in ptList)))

