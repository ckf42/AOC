import AOCInit
import util
import sympy as sp
import itertools as it

if __name__ != '__main__':
    exit()

inp = '29000000'
inp = int(inp)

# part 1
def sumFact(fd):
    return util.prod((p ** (f + 1) - 1) / (p - 1) for p, f in fd.items())

# print(util.firstSuchThat(it.count(2), lambda n: sumFact(sp.factorint(n)) * 10 >= inp))

# part 2
# ?
