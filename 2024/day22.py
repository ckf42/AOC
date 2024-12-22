import AOCInit
import util

from collections import Counter

if __name__ != '__main__':
    exit()

inp = util.getInput(d=22, y=2024)

initSecrets = tuple(int(x) for x in inp.splitlines())

pruneMask = 16777216 - 1

def getNextSecret(x):
    x = (x ^ (x << 6)) & pruneMask
    x = (x ^ (x >> 5)) & pruneMask
    x = (x ^ (x << 11)) & pruneMask
    return x

part1Sum = 0
totalCounter: Counter[int] = Counter()
for s in initSecrets:
    counter: Counter[int] = Counter()
    oldPrice = s % 10
    coor = 0
    for i in range(2000):
        ss = getNextSecret(s)
        price = ss % 10
        coor = coor // 19 + (price - oldPrice + 9) * (19 ** 3)
        if i >= 3 and coor not in counter:
            counter[coor] = price
        s = ss
        oldPrice = price
    part1Sum += s
    totalCounter += counter
print(part1Sum)
print(totalCounter.most_common(1)[0][1])

