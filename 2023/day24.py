import AOCInit
import util
import sympy as sp

if __name__ != '__main__':
    exit()

inp = util.getInput(d=24, y=2023)

stones = tuple(
        util.splitIntoGp(util.getInts(line), 3)
        for line in inp.splitlines())
stoneCount = len(stones)

# part 1
detectDom = (200000000000000, 400000000000000)

crosses = 0
for i in range(stoneCount):
    ap, av = stones[i]
    for j in range(i + 1, stoneCount):
        bp, bv = stones[j]
        det = av[1] * bv[0] - av[0] * bv[1]
        if det == 0:
            continue
        t = (-bv[1] * (bp[0] - ap[0]) + bv[0] * (bp[1] - ap[1])) / det
        s = (-av[1] * (bp[0] - ap[0]) + av[0] * (bp[1] - ap[1])) / det
        if t >= 0 and s >= 0 \
                and detectDom[0] <= ap[0] + t * av[0] <= detectDom[1] \
                and detectDom[0] <= ap[1] + t * av[1] <= detectDom[1]:
            crosses += 1
print(crosses)


# part 2
# TODO: check if first 3 velocities parallel. Here it just works(TM)
# TODO: solution without sympy
p = sp.var('x y z')
v = sp.var('vx vy vz')
t = sp.var('t1 t2 t3')
equs = list()
for i in range(3):
    ps, vs = stones[i]
    for d in range(3):
        equs.append(p[d] - ps[d] + t[i] * (v[d] - vs[d]))
res = sp.solve(equs, *p, *v, *t, dict=True)
assert len(res) == 1, "Too many solutions"  # TODO: how to filter?
print(sum(res[0][var] for var in p))


