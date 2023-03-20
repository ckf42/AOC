import AOCInit
import util
from itertools import groupby

if __name__ != '__main__':
    exit()

inp = util.getInput(d=4, y=2019)
(s, e) = tuple(map(int, inp.strip().split('-')))

part1Count = 0
part2Count = 0

for n in util.inclusiveRange(max(int(1e5), s), min(int(1e6) - 1, e)):
    lastChar = None
    part1Valid = False
    part2Valid = False
    for p in ((k, len(tuple(t))) for k, t in groupby(str(n))):
        if lastChar is not None and lastChar > p[0]:
            part1Valid = part2Valid = False
            break
        lastChar = p[0]
        part1Valid |= p[1] >= 2
        part2Valid |= p[1] == 2
    part1Count += part1Valid
    part2Count += part2Valid

# part 1
print(part1Count)

# part 2
print(part2Count)


