import AOCInit
import util

import re

if __name__ != '__main__':
    exit()

inp = util.getInput(d=3, y=2024)

# part 1
mulPatt = re.compile(r'mul\((\d+),(\d+)\)')
print(sum(int(a) * int(b) for a, b in mulPatt.findall(inp)))

# part 2
n = len(inp)
ptr = 0
res = 0
while ptr != -1:
    loc = inp.find("don't()", ptr)
    if loc == -1:
        loc = n
    res += sum(int(a) * int(b) for a, b in mulPatt.findall(inp[ptr:loc]))
    ptr = inp.find("do()", loc)
print(res)

