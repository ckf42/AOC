import AOCInit
import util
from functools import reduce
from operator import xor

if __name__ != '__main__':
    exit()

inp = util.getInput(d=6, y=2022)
l = len(inp)

def toMsk(c):
    return 1 << (ord(c) - ord('a'))

# part 1
# print(util.firstSuchThat(range(l - 4), lambda i: len(set(inp[i:i + 4])) == 4)[0] + 4)
# idea from Matt Keeter
# benchmark: util.firstSuchThat 357us, findWindow 340us

def findWindow(wSize):
    msk = reduce(xor, map(toMsk, inp[:wSize]))
    if msk.bit_count() == wSize:
        return wSize
    else:
        for i in range(wSize, l):
            msk ^= toMsk(inp[i]) ^ toMsk(inp[i - wSize])
            if msk.bit_count() == wSize:
                return i + 1
        return None
print(findWindow(4))

# part 2
# 
# print(util.firstSuchThat(range(l - 14), lambda i: len(set(inp[i:i + 14])) == 14)[0] + 14)
# benchmark: util.firstSuchThat 1.42ms, findWindow 676us
print(findWindow(14))

