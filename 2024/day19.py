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


# part 1
counter = 0
for d in demand:
    buff = [trie]
    for c in d:
        newBuff = list()
        for ptr in buff:
            if c in ptr:
                if ptr[c] not in newBuff:
                    newBuff.append(ptr[c])
                if '' in ptr[c] and trie not in newBuff:
                    newBuff.append(trie)
        buff = newBuff
    if trie in buff:
        counter += 1
print(counter)


# part 2
counter = 0
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
    counter += buffDict[""]
print(counter)
