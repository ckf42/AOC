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


prs = sorted((d(pts[i], pts[j]), i, j) for i in range(n) for j in range(i + 1, n))
for idx, (_, i, j) in enumerate(prs):
    if not djs.isSameGroup(i, j):
        djs.union(i, j)
    # part 1
    if idx == 1000 - 1:
        sizes = [len(gp) for gp in djs.getGroups()]
        sizes.sort(reverse=True)
        print(util.prod(sizes[:3]))
    # part 2
    if len(next(djs.getGroups())) == n:
        print(pts[i][0] * pts[j][0])
        break
