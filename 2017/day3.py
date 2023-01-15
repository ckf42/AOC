import AOCInit
import util
from math import ceil

if __name__ != '__main__':
    exit()

inp = int(util.getInput(d=3, y=2017).strip())

# part 1
def getLoc(n):
    # | -> x
    # V
    # y
    if n == 1:
        return (0, 0)
    a = ceil(n ** (1 / 2))
    if a % 2 == 0:
        a += 1
    aa = a ** 2
    a2 = a // 2
    (q, r) = divmod(aa - n, a - 1)
    if q == 0:
        return (a2 - r, a2)
    elif q == 1:
        return (-a2, a2 - r)
    elif q == 2:
        return (r - a2, -a2)
    else:
        # q == 3
        return (a2, r - a2)

print(sum(map(abs, getLoc(inp))))

# part 2
record = {util.Point(0, 0): 1}
directions = tuple(map(util.Point.fromIterable, util.integerLattice(2, 1, util.inf)))
def getVal(n):
    loc = util.Point.fromIterable(getLoc(n))
    if loc not in record:
        record[loc] = sum(record.get(loc + d, 0) for d in directions)
    return record[loc]

idx = 1
while (s := getVal(idx)) <= inp:
    idx += 1
print(record[util.Point.fromIterable(getLoc(idx))])

