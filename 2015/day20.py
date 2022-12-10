import AOCInit
import util
import sympy as sp
import itertools as it

# TODO: need faster algorithm

if __name__ != '__main__':
    exit()

inp = '123'
inp = int(inp)

# part 1
print(util.firstSuchThat(it.count(2),
                         lambda n: sp.divisor_sigma(n, 1) * 10 >= inp)[1])

# part 2
print(util.firstSuchThat(it.count(2),
                         lambda n: sum(filter(lambda d: d * 50 >= n,
                                              sp.divisors(n))) * 11 >= inp)[1])

