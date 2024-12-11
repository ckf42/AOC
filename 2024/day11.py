import AOCInit
import util

from functools import cache

if __name__ != '__main__':
    exit()

inp = util.getInput(d=11, y=2024)

nums = util.getInts(inp)

def makeNewStones(x):
    if x == 0:
        return (1,)
    if len(s := str(x)) & 1:
        return (x * 2024,)
    return (int(s[:len(s) // 2]), int(s[len(s) // 2:]))

@cache
def genLen(x, count):
    if count == 0:
        return 1
    return sum(genLen(y, count - 1) for y in makeNewStones(x))

# part 1
print(sum(genLen(x, 25) for x in nums))

# part 2
print(sum(genLen(x, 75) for x in nums))

