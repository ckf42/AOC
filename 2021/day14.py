import AOCInit
import util
from collections import defaultdict

if __name__ != '__main__':
    exit()

inp = util.getInput(d=14, y=2021)

(initPoly, ruleLines) = inp.split('\n\n')
rules = {
    parts[0]: parts[1]
    for line in ruleLines.splitlines()
    if (parts := line.split(' -> '))
}

endChars = initPoly[0] + initPoly[-1]
twoTupleCount: defaultdict[str, int] = defaultdict(int)
for i in range(len(initPoly) - 1):
    twoTupleCount[initPoly[i:i + 2]] += 1

# part 1
newTwoTupleCount: defaultdict[str, int] = defaultdict(int)
for _ in range(10):
    newTwoTupleCount.clear()
    for k, v in twoTupleCount.items():
        c = rules[k]
        newTwoTupleCount[k[0] + c] += v
        newTwoTupleCount[c + k[1]] += v
    twoTupleCount = newTwoTupleCount.copy()
occurrence: defaultdict[str, int] = defaultdict(int)
for c in endChars:
    occurrence[c] += 1
for k, v in twoTupleCount.items():
    for c in k:
        occurrence[c] += v
print((max(occurrence.values()) - min(occurrence.values())) // 2)

# part 2
for _ in range(40 - 10):
    newTwoTupleCount.clear()
    for k, v in twoTupleCount.items():
        c = rules[k]
        newTwoTupleCount[k[0] + c] += v
        newTwoTupleCount[c + k[1]] += v
    twoTupleCount = newTwoTupleCount.copy()
occurrence.clear()
for c in endChars:
    occurrence[c] += 1
for k, v in twoTupleCount.items():
    for c in k:
        occurrence[c] += v
print((max(occurrence.values()) - min(occurrence.values())) // 2)



