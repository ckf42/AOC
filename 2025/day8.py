import AOCInit
import util

if __name__ != "__main__":
    exit()


inp = util.getInput(d=8, y=2025)

pts = [tuple(util.getInts(l)) for l in inp.splitlines()]
n = len(pts)
djs = util.DisjointSet(n)


def d(x, y):
    return sum((a - b) ** 2 for a, b in zip(x, y))


for idx, (i, j) in enumerate(
    sorted(
        ((i, j) for i in range(n) for j in range(i + 1, n)),
        key=lambda pr: d(pts[pr[0]], pts[pr[1]]),
    )
):
    if not djs.isSameGroup(i, j):
        djs.union(i, j)
    # part 1
    if idx == 1000 - 1:
        print(util.prod(util.findMaxK(3, (len(gp) for gp in djs.getGroups()))))
    # part 2
    if len(next(djs.getGroups())) == n:
        print(pts[i][0] * pts[j][0])
        break
