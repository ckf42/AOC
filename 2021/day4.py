import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=4, y=2021)

callSeq = util.getInts(inp.split('\n\n', maxsplit=1)[0])
boards = util.splitIntoGp(util.getInts(inp.split('\n\n', maxsplit=1)[1]),
                          25,
                          allowRemain=False)
boardCount = len(boards)

def bingo(idxSet):
    return any(all((i + 5 * j) in idxSet for j in range(5)) for i in range(5)) \
            or any(all((j + 5 * i) in idxSet for j in range(5)) for i in range(5))

# part 1
boardSets = tuple(map(frozenset, boards))
calledIndices = [set() for _ in boards]
part1Answered = False

boardIndices = set(range(boardCount))
score = -1
for nidx, n in enumerate(callSeq):
    idxToDrop = set()
    for i in boardIndices:
        if n in boardSets[i]:
            calledIndices[i].add(boards[i].index(n))
            if bingo(calledIndices[i]):
                score = sum(n
                            for n in boardSets[i]
                            if n not in frozenset(callSeq[:nidx + 1])) * n
                idxToDrop.add(i)
                if not part1Answered:
                    print(score)
                    part1Answered = True
    boardIndices.difference_update(idxToDrop)
print(score)



