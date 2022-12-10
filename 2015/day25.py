import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInts(util.getInput(d=25, y=2015))

iterCount = (lambda n: n * (n - 1) // 2)(inp[0] + inp[1] - 1) + inp[1]
seed = 20151125
p = 33554393
a = 252533

# part 1
print((seed * pow(a, iterCount - 1, mod=p)) % p)

# part 2
# ?
# require 49 stars to unlock
