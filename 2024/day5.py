import AOCInit
import util

from collections import defaultdict
from functools import cmp_to_key

if __name__ != '__main__':
    exit()

inp = util.getInput(d=5, y=2024)

# part 1
rulesText, sectOrderText = inp.split('\n\n')
rules = tuple(util.getInts(line) for line in rulesText.splitlines())
sects = tuple(util.getInts(line) for line in sectOrderText.splitlines())

edges: defaultdict[int, set[int]] = defaultdict(set)
for a, b in rules:
    edges[a].add(b)

corrOrder = [False] * len(sects)
def isCorrOrder(sectOrder: tuple[int, ...]) -> bool:
    n = len(sectOrder)
    for i in range(n - 1):
        for j in range(i + 1, n):
            if sectOrder[i] in edges[sectOrder[j]]:
                return False
    return True

total = 0
for i, sect in enumerate(sects):
    if isCorrOrder(sect):
        corrOrder[i] = True
        total += sect[len(sect) // 2]
print(total)

# part 2
total = 0
for i, sect in enumerate(sects):
    if not corrOrder[i]:
        newOrder = sorted(
            sect,
            key=cmp_to_key(lambda a, b: -1 if b in edges[a] else 0)
        )
        total += newOrder[len(newOrder) // 2]
print(total)

