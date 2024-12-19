import AOCInit
import util

from collections import defaultdict

if __name__ != '__main__':
    exit()

inp = util.getInput(d=19, y=2024)

available = tuple(
    inp.split('\n\n')[0].split(', ')
)
demand = tuple(inp.split('\n\n')[1].splitlines())

trie = dict()
nodeMap = {"": trie}
for towel in available:
    ptr = trie
    for i, c in enumerate(towel):
        if c not in ptr:
            ptr[c] = dict()
            ptr[c][', '] = towel[:i + 1]
            nodeMap[towel[:i + 1]] = ptr[c]
        ptr = ptr[c]
    ptr[''] = True


part1Counter = 0
part2Counter = 0
for d in demand:
    buffDict = defaultdict(int)
    buffDict[""] = 1
    for c in d:
        newBuffDict = defaultdict(int)
        for seg, freq in buffDict.items():
            ptr = nodeMap[seg]
            if c in ptr:
                newBuffDict[ptr[c][', ']] += freq
                if '' in ptr[c]:
                    newBuffDict[""] += freq
        buffDict = newBuffDict
    part1Counter += "" in buffDict
    part2Counter += buffDict[""]
print(part1Counter)
print(part2Counter)

