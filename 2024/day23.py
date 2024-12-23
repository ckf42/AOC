import AOCInit
import util

from collections import defaultdict

if __name__ != '__main__':
    exit()

inp = util.getInput(d=23, y=2024)

edges = defaultdict(list)
for line in inp.splitlines():
    b, c = line.split('-')
    edges[b].append(c)
    edges[c].append(b)
nodes = tuple(edges.keys())

# part 1
cliques = set()
for a in nodes:
    if not a.startswith('t'):
        continue
    n = len(edges[a])
    for i in range(n):
        for j in range(i + 1, n):
            b = edges[a][i]
            c = edges[a][j]
            if b in edges[c]:
                cliques.add(tuple(sorted((a, b, c))))
print(len(cliques))


# part 2
maxCliqueNodes = max(util.findMaxCliques(edges), key=len)
print(','.join(sorted(maxCliqueNodes)))


