import AOCInit
import util
from collections import defaultdict
from functools import cache

if __name__ != '__main__':
    exit()

inp = util.getInput(d=7, y=2020)

rules = {
        sp[0].rsplit(maxsplit=1)[0]: \
                    tuple(
                        (int(cont.split(maxsplit=1)[0]),
                         ' '.join(cont.split()[1:-1]))
                        for cont in sp[1].split(', ')
                    )
                    if 'no other' not in sp[1]
                    else tuple()
        for line in inp.splitlines()
        if len((sp := line.split(' contain '))) != 0
}

# part 1
reverseInclusion = defaultdict(set)
for r, c in rules.items():
    for item in c:
        reverseInclusion[item[1]].add(r)
countedBags: set[str] = set()
newBags: frozenset[str] = frozenset(('shiny gold',))
while len(newBags) != 0:
    countedBags.update(newBags)
    newBags = frozenset(nb
                        for b in newBags
                        for nb in reverseInclusion[b])
print(len(countedBags) - 1) # exclude shiny gold

# part 2
@cache
def getBagCount(bagName: str) -> int:
    return sum(cont[0] * (getBagCount(cont[1]) + 1) for cont in rules[bagName])

print(getBagCount('shiny gold'))

