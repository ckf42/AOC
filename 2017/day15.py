import AOCInit
import util

if __name__ != '__main__':
    exit()

# TODO: need optimization. took ~53s for both parts
# is it possible to optimize?

inp = util.getInput(d=15, y=2017)

(aSeed, bSeed) = util.getInts(inp)
m = 2147483647
msk = (1 << 16) - 1

def aGen(s, p=1):
    while True:
        s = (s * 16807) % m
        if p == 1 or s & 3 == 0:
            yield s % msk

def bGen(s, p=1):
    while True:
        s = (s * 48271) % m
        if p == 1 or s & 7 == 0:
            yield s % msk

# part 1
a = aGen(aSeed)
b = bGen(bSeed)
print(sum(next(a) == next(b) for _ in range(40000000)))

# part 2
counter = 0
a = aGen(aSeed, p=2)
b = bGen(bSeed, p=2)
print(sum(next(a) == next(b) for _ in range(5000000)))

