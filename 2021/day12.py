import AOCInit
import util
from collections import defaultdict

if __name__ != '__main__':
    exit()

inp = util.getInput(d=12, y=2021)

edges: defaultdict[str, set[str]] = defaultdict(set)
for line in inp.splitlines():
    (a, b) = line.split('-')
    edges[a].add(b)
    edges[b].add(a)

# part 1
stack: list[tuple[str, ...]] = list()
stack.append(('start',))
visited: set[tuple[str, ...]] = set()
pathCount = 0
while len(stack) != 0:
    pathNodes = stack.pop()
    if pathNodes in visited:
        continue
    if pathNodes[-1] == 'end':
        pathCount += 1
        continue
    pathNodeSet = frozenset(pathNodes)
    for nei in edges[pathNodes[-1]]:
        if nei.isupper() or nei not in pathNodeSet:
            stack.append(pathNodes + (nei,))
print(pathCount)

# part 2
stack2: list[tuple[tuple[str, ...], bool]] = list()
stack2.append((('start',), False))
visited.clear()
pathCount = 0
while len(stack2) != 0:
    (pathNodes, nodeRepeated) = stack2.pop()
    if pathNodes in visited:
        continue
    visited.add(pathNodes)
    if pathNodes[-1] == 'end':
        pathCount += 1
        continue
    pathNodeSet = frozenset(pathNodes)
    for nei in edges[pathNodes[-1]]:
        if nei.isupper() or nei not in pathNodeSet:
            stack2.append((pathNodes + (nei,), nodeRepeated))
        elif not nodeRepeated and nei != 'start':
            stack2.append((pathNodes + (nei,), True))
print(pathCount)


