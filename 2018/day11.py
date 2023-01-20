import AOCInit
import util
from functools import cache

if __name__ != '__main__':
    exit()

inp = util.getInput(d=11, y=2018)

serialNum = int(inp)
dim = 300

@cache
def getLevel(x, y):
    rId = x + 10
    return (((rId * y + serialNum) * rId) % 1000) // 100 - 5

@cache
def partialSum(x, y):
    if 0 in (x, y):
        return 0
    else:
        return partialSum(x - 1, y) \
                + partialSum(x, y - 1) \
                - partialSum(x - 1, y - 1) \
                + getLevel(x, y)

@cache
def getMaxWithSize(size):
    maxPt = None
    currMax = -util.inf
    for i in range(1, dim + 2 - size):
        for j in range(1, dim + 2 - size):
            valSum = partialSum(i + size - 1, j + size - 1) \
                    + partialSum(i - 1, j - 1) \
                    - partialSum(i + size - 1, j - 1) \
                    - partialSum(i - 1, j + size - 1)
            if currMax < valSum:
                currMax = valSum
                maxPt = (i, j)
    return (maxPt, currMax)

# part 1
print(','.join(map(str, getMaxWithSize(3)[0])))

# part 2
# TODO: optimize. Currently takes ~12s
maxSize = util.argmax(range(1, dim + 1), lambda s: getMaxWithSize(s)[1])
print(','.join(map(str, getMaxWithSize(maxSize)[0] + (maxSize,))))

