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

N = 19 ** 4
M = 19 ** 3
part1Sum = 0
totalCounter: list[int] = [0] * N
for s in initSecrets:
    oldPrice = s % 10
    coor = 0
    seen = [False] * N
    for i in range(2000):
        ss = getNextSecret(s)
        price = ss % 10
        coor = coor // 19 + (price - oldPrice + 9) * M
        if i >= 3 and not seen[coor]:
            totalCounter[coor] += price
            seen[coor] = True
        s = ss
        oldPrice = price
    part1Sum += s
print(part1Sum)
print(max(totalCounter))

