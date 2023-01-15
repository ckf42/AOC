import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = """\
p=< 3,0,0>, v=< 2,0,0>, a=<-1,0,0>
p=< 4,0,0>, v=< 0,0,0>, a=<-2,0,0>\
"""
inp = util.getInput(d=20, y=2017)

particles = tuple(
    tuple(map(util.Point.fromIterable, numGps))
    for l in inp.splitlines()
    if (numGps := util.splitIntoGp(util.getInts(l), 3))
)
l = len(particles)

# part 1
print(util.argmin(util.rangeLen(particles), lambda i: particles[i][2].norm(1)))

# part 2
def getLoc(idx, t):
    part = particles[idx]
    return part[0] + t * part[1] + t * (t + 1) // 2 * part[2]

def solTime(p, v, a):
    # sol non-neg int equ a n**2 / 2 + (v + a / 2) * n + p = 0
    if a == 0:
        if v == 0:
            return {0} if p == 0 else set()
        else:
            return {-p // v} if p % v == 0 and p * v <= 0 else set()
    deltaSquare = (2 * v + a) ** 2 - 8 * a * p
    if deltaSquare < 0:
        return set()
    delta = deltaSquare ** (1 / 2)
    nList = list(n
                 for sd in set((delta, -delta))
                 if (n := round((- 2 * v - a + sd) / (2 * a))) >= 0)
    return set(filter(lambda n: a * n ** 2 + (2 * v + a) * n + 2 * p == 0,
                      nList))

def hitTime(idx1, idx2):
    deltas = tuple(tuple(particles[idx1][prop][d] - particles[idx2][prop][d]
                         for prop in range(3))
                   for d in range(3))
    hitTimeSet = set.intersection(*(solTime(*delta) for delta in deltas))
    return None if len(hitTimeSet) == 0 else min(hitTimeSet)

hitTimeRecord: dict[int, dict[tuple[int, int, int], set[int]]] = dict()
for i in range(l - 1):
    for j in range(i + 1, l):
        if (t := hitTime(i, j)) is not None:
            if t not in hitTimeRecord:
                hitTimeRecord[t] = dict()
            loc = getLoc(i, t)
            if loc not in hitTimeRecord[t]:
                hitTimeRecord[t][loc] = set()
            hitTimeRecord[t][loc].update((i, j))
stillAlive = [True for _ in range(l)]
for t in sorted(hitTimeRecord.keys()):
    for partIdxSet in hitTimeRecord[t].values():
        hittingParticles = tuple(filter(lambda idx: stillAlive[idx], partIdxSet))
        if len(hittingParticles) > 1:
            for pIdx in hittingParticles:
                stillAlive[pIdx] = False
print(sum(stillAlive))

