import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=3, y=2021)

# part 1
inputSeq = inp.splitlines()
bitSeq = tuple(tuple(map(int, line))
               for line in util.transpose(inp.splitlines()))
bitCount = len(bitSeq[0])
gamma = util.fromBase(tuple(1
                            if sum(bseq) * 2 >= bitCount
                            else 0
                            for bseq in bitSeq),
                      b=2)
delta = ((1 << len(bitSeq)) - 1) ^ gamma
print(gamma * delta)

# part 2
vals = list()

idxSet = set(range(len(inputSeq)))
for i in range(bitCount):
    if len(idxSet) == 1:
        break
    b = '1' if sum(map(int,
                       (inputSeq[idx][i]
                        for idx in idxSet))) * 2 >= len(idxSet) else '0'
    idxSet = set(filter(lambda idx: inputSeq[idx][i] == b, idxSet))
assert len(idxSet) == 1
vals.append(int(inputSeq[idxSet.pop()], base=2))

idxSet = set(range(len(inputSeq)))
for i in range(bitCount):
    if len(idxSet) == 1:
        break
    b = '1' if sum(map(int,
                       (inputSeq[idx][i]
                        for idx in idxSet))) * 2 >= len(idxSet) else '0'
    idxSet = set(filter(lambda idx: inputSeq[idx][i] != b, idxSet))
assert len(idxSet) == 1
vals.append(int(inputSeq[idxSet.pop()], base=2))

print(util.prod(vals))

