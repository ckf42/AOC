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

trie = util.Trie(available)

part1Counter = 0
part2Counter = 0
for d in demand:
    buffDict: defaultdict[int, int] = defaultdict(int)
    buffDict[0] = 1
    for c in d:
        newBuffDict: defaultdict[int, int] = defaultdict(int)
        for ptr, freq in buffDict.items():
            nextPtr = trie.advance(c, ptr)
            if nextPtr is not None:
                newBuffDict[nextPtr] += freq
                if trie.hasItemAt(nextPtr):
                    newBuffDict[0] += freq
        buffDict = newBuffDict
    part1Counter += 0 in buffDict
    part2Counter += buffDict[0]
print(part1Counter)
print(part2Counter)

