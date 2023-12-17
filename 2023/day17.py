import AOCInit
import util

# TODO: speed up

if __name__ != '__main__':
    exit()

inp = util.getInput(d=17, y=2023)

heatmap = tuple(tuple(int(c) for c in line)
                for line in inp.splitlines())
dim = (len(heatmap), len(heatmap[0]))

# part 1
# takes ~5s
def nb(st):
    node, combo, prev = st
    nblst = list()
    for pt in util.nearby2DGridPts(node, bd=dim, isL1=True):
        if pt == prev:
            continue
        sameDir = prev[0] + pt[0] == 2 * node[0] and prev[1] + pt[1] == 2 * node[1]
        if combo == 3 and sameDir:
            continue
        nblst.append((pt, (combo + 1) if sameDir else 1, node))
    return nblst

print(util.dijkstra(
    ((0, 0), 0, (0, 0)),  # pos, straight combo, prev
    lambda nst, ost, oc: oc + heatmap[nst[0][0]][nst[0][1]],
    nb,
    lambda st: st[0] == (dim[0] - 1, dim[1] - 1),
    lambda st: dim[0] - 1 - st[0][0] + dim[1] - 1 - st[0][1]
    )[-1])


# part 2
# takes ~15s
def nb2(st):
    node, combo, prev = st
    nblst = list()
    for pt in util.nearby2DGridPts(node, bd=dim, isL1=True):
        if pt == prev:
            continue
        sameDir = prev[0] + pt[0] == 2 * node[0] and prev[1] + pt[1] == 2 * node[1]
        if combo >= 10 and sameDir:
            continue
        if combo < 4 and not sameDir:
            continue
        nblst.append((pt, (combo + 1) if sameDir else 1, node))
    # print(st, nblst)
    return nblst

print(util.dijkstra(
    ((0, 0), 10, (0, 0)),  # pos, straight combo, prev
    lambda nst, ost, oc: oc + heatmap[nst[0][0]][nst[0][1]],
    nb2,
    lambda st: st[1] >= 4 and (st[0] == (dim[0] - 1, dim[1] - 1)),
    lambda st: dim[0] - 1 - st[0][0] + dim[1] - 1 - st[0][1]
    )[-1])

