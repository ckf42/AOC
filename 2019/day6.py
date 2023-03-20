import AOCInit
import util
from collections import defaultdict

if __name__ != '__main__':
    exit()

inp = util.getInput(d=6, y=2019)

# part 1
parent = {'COM': 'COM'}
children = defaultdict(list)
for line in inp.splitlines():
    (p, c) = line.split(')')
    children[p].append(c)
    parent[c] = p
dep = {'COM': 0}
accum = 0
stack = children['COM'].copy()
while len(stack) != 0:
    pt = stack.pop()
    dep[pt] = dep[parent[pt]] + 1
    accum += dep[pt]
    stack.extend(children[pt])
print(accum)

# part 2
nodeIdx = {n: i for i, n in enumerate(parent.keys())}
djs = util.DisjointSet(len(nodeIdx))

def ocla(u, lca=None):
    if lca is not None:
        return lca
    for v in children.get(u, tuple()):
        lca = ocla(v, lca)
        if lca is not None:
            return lca
        djs.union(nodeIdx[u], nodeIdx[v])
    if djs.isSameGroup(nodeIdx['YOU'], nodeIdx['SAN']):
        return u
    return None

lca = ocla('COM')
assert lca is not None
pathLen = 0
for pt in ('YOU', 'SAN'):
    ptr = pt
    while ptr != lca:
        ptr = parent[ptr]
        pathLen += 1
print(pathLen - 2)

