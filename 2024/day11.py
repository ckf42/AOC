import AOCInit
import util

from functools import cache

if __name__ != '__main__':
    exit()

inp = util.getInput(d=11, y=2024)

nums = util.getInts(inp)

@cache
def makeNewStone(x):
    if x == 0:
        return (1,)
    s = str(x)
    if len(s) & 1:
        return (x * 2024,)
    return (int(s[:len(s) // 2]), int(s[len(s) // 2:]))

# part 1
freqDict: dict[int, int] = dict()
for x in nums:
    freqDict[x] = freqDict.get(x, 0) + 1
for _ in range(25):
    newFreqDict: dict[int, int] = dict()
    for x, fq in freqDict.items():
        for y in makeNewStone(x):
            newFreqDict[y] = newFreqDict.get(y, 0) + fq
    freqDict = newFreqDict
print(sum(freqDict.values()))

# part 2
for _ in range(75 - 25):
    newFreqDict = dict()
    for x, fq in freqDict.items():
        for y in makeNewStone(x):
            newFreqDict[y] = newFreqDict.get(y, 0) + fq
    freqDict = newFreqDict
print(sum(freqDict.values()))

# timer = util.Timer()
# for _ in range(10000 - 75):
#     newFreqDict = dict()
#     for x, fq in freqDict.items():
#         for y in makeNewStone(x):
#             newFreqDict[y] = newFreqDict.get(y, 0) + fq
#     freqDict = newFreqDict
# print(sum(freqDict.values()))
# timer.stop()

