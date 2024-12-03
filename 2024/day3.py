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
doPatt = re.compile(r'do\(\)')
dontPatt = re.compile(r"don't\(\)")
n = len(inp)
ptr = 0
res = 0
while ptr < n:
    m = dontPatt.search(inp[ptr:])
    loc = n
    if m is not None:
        loc = ptr + m.start()
    res += sum(int(a) * int(b) for a, b in mulPatt.findall(inp[ptr:loc]))
    m = doPatt.search(inp[loc:])
    if m is None:
        break
    ptr = loc + m.start()
print(res)

