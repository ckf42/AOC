import AOCInit
import util
from functools import cache

if __name__ != '__main__':
    exit()

inp = util.getInput(d=1, y=2019)
masses = util.getInts(inp)

# part 1
print(sum(map(lambda n: n // 3 - 2, masses)))


# part 2
@cache
def getFuel(n):
    if n < 9:
        return 0
    else:
        nn = n // 3 - 2
        return nn + getFuel(nn)

print(sum(map(getFuel, masses)))

