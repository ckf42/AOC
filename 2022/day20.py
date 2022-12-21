import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInts(util.getInput(d=20, y=2022))

# part 1
l = len(inp)

def mixing(taggedList):
    for orderToMove in range(l):
        idx = util.firstIdxSuchThat(taggedList, lambda t: t[0] == orderToMove)
        offset = taggedList[idx][1]
        # offset = abs(offset) % (l - 1) # loop, off by one
        if offset == 0:
            continue
        item = taggedList[idx]
        # replace it with slicing
        taggedList = taggedList[idx + 1:] + taggedList[:idx]
        taggedList.insert(offset % (l - 1), item)
    return taggedList

taggedSeq = mixing(list(enumerate(inp)))
idx = util.firstIdxSuchThat(taggedSeq, lambda t: t[1] == 0)
print(sum(util.cycInd(taggedSeq, idx + i)[1] for i in (1000, 2000, 3000)))


# part 2
k = 811589153
taggedSeq = list(enumerate((i * k for i in inp)))
for _ in range(10):
    taggedSeq = mixing(taggedSeq)
idx = util.firstIdxSuchThat(taggedSeq, lambda t: t[1] == 0)
print(sum(util.cycInd(taggedSeq, idx + i)[1] for i in (1000, 2000, 3000)))

