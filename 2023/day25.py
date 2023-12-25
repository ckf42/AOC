import AOCInit
import util
from collections import defaultdict
import igraph as ig

if __name__ != '__main__':
    exit()

inp = util.getInput(d=25, y=2023)

compo = defaultdict(set)
for line in inp.splitlines():
    ls = line.split()
    d = ls[0][:-1]
    for c in ls[1:]:
        compo[d].add(c)
        compo[c].add(d)
nodes = set()
for c, nb in compo.items():
    nodes.add(c)
    nodes.update(nb)

# part 1
# TODO: solution without ig?
nodeToId = {n: i for i, n in enumerate(nodes)}
g = ig.Graph(len(nodes))
for c, nb in compo.items():
    for n in nb:
        g.add_edge(nodeToId[c], nodeToId[n])
g = g.simplify()
cut = g.mincut()
assert len(cut.cut) == 3
assert len(cut.partition) == 2
print(util.prod(len(p) for p in cut.partition))

# part 2
# no part 2

