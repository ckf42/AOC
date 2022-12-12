import AOCInit
import util
import sympy as sp
import itertools as it

if __name__ != '__main__':
    exit()

inp = '1234567'
inp = int(inp)

# part 1
# TODO: need faster algorithm. Is it possible to avoid doing factorization?
# TODO: try using the same method as part 2 with iteratively deepening `factorRatio`
# print(util.firstSuchThat(it.count(2),
                         # lambda n: sp.divisor_sigma(n, 1) * 10 >= inp)[1])

# part 2
# print(util.firstSuchThat(it.count(2),
                         # lambda n: sum(filter(lambda d: d * 50 >= n,
                                              # sp.divisors(n))) * 11 >= inp)[1])

# thank you @zfengg for the solution
factorRatio = 50

def s(n):
    return 1 + sum(dm[0]
                   for i in range(2, min(n, factorRatio + 1))
                   if (dm := divmod(n, i)) and dm[1] == 0)

print(util.firstSuchThat(it.count(2), lambda n: s(n) * 11 >= inp)[1])

