import AOCInit
import util
from collections import defaultdict
from graphlib import TopologicalSorter

if __name__ != "__main__":
    exit()


inp = util.getInput(d=11, y=2025)

edges = defaultdict(list)
for line in inp.splitlines():
    dev = line.split(":", maxsplit=1)[0]
    outs = line.split(":", maxsplit=1)[1].strip().split()
    for o in outs:
        edges[dev].append(o)

ordering = list(TopologicalSorter(edges).static_order())[::-1]
nameToIdx = {v: i for i, v in enumerate(ordering)}

# part 1
def countPaths(sourceIdx, targetIdx):
    count = defaultdict(int)
    count[sourceIdx] = 1
    for idx in range(sourceIdx, targetIdx):
        for nb in edges[ordering[idx]]:
            count[nameToIdx[nb]] += count[idx]
    return count[targetIdx]


print(countPaths(nameToIdx["you"], nameToIdx["out"]))

# part 2

firstIdx = ordering.index('dac')
secondIdx = ordering.index('fft')
if firstIdx > secondIdx:
    firstIdx, secondIdx = secondIdx, firstIdx
print(util.prod([
    countPaths(nameToIdx['svr'], firstIdx),
    countPaths(firstIdx, secondIdx),
    countPaths(secondIdx, nameToIdx['out']),
]))

