import AOCInit
import util

from collections import deque, Counter

if __name__ != '__main__':
    exit()

inp = util.getInput(d=22, y=2024)

initSecrets = tuple(int(x) for x in inp.splitlines())

pruneMod = 16777216
pruneMask = pruneMod - 1

def getNextSecret(x):
    x = (x ^ (x << 6)) & pruneMask
    x = (x ^ (x >> 5)) & pruneMask
    x = (x ^ (x << 11)) & pruneMask
    return x

part1Sum = 0
totalCounter: Counter[tuple[int, int, int, int]] = Counter()
for s in initSecrets:
    counter: Counter[tuple[int, int, int, int]] = Counter()
    q: deque[int] = deque(maxlen=4)
    for _ in range(2000):
        ss = getNextSecret(s)
        q.append((ss % 10) - (s % 10))
        seq = tuple(q)
        if seq not in counter and len(seq) == 4:
            counter[seq] = ss % 10
        s = ss
    part1Sum += s
    totalCounter += counter
print(part1Sum)
print(totalCounter.most_common(1))

