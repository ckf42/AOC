import AOCInit
import util
from sympy.ntheory.modular import crt

if __name__ != '__main__':
    exit()

inp = util.getInput(d=15, y=2016)
discConfig = tuple((gp[1], (-gp[0] - gp[3]) % gp[1])
                   for gp in util.splitIntoGp(util.getInts(inp), 4))
(m, r) = util.transpose(discConfig)

# part 1
print(crt(m, r)[0])

# part 2
m = m + (11,)
r = r + ((-len(m) - 0) % 11,)
print(crt(m, r)[0])

