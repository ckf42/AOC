import AOCInit
import util

import re

if __name__ != '__main__':
    exit()

inp = util.getInput(d=4, y=2024)

lines = inp.splitlines()
n = len(lines)
m = len(lines[0])  # assume rect

patts = (re.compile("(?=(XMAS))"), re.compile("(?=(SAMX))"))

# part 1
linesTransposed = tuple(''.join(line) for line in util.transpose(lines))
diagLines = tuple(''.join(line) for line in util.diagonals(lines))
otherDiagLines = tuple(''.join(line) for line in util.diagonals(lines, isAntiDiag=True))
count = sum(
    len(patt.findall(line))
    for patt in patts
    for lineGps in (lines, linesTransposed, diagLines, otherDiagLines)
    for line in lineGps
)
print(count)

# part 2
count = 0
for i in range(1, n - 1):
    ptr = -1
    while True:
        ptr = lines[i].find('A', ptr + 1)
        if ptr == -1:
            break
        # print(ptr)
        if ptr in (0, m - 1):
            continue
        if all(lines[i - 1][jj] == 'M' for jj in (ptr - 1, ptr + 1)) \
                and all(lines[i + 1][jj] == 'S' for jj in (ptr - 1, ptr + 1)):
            count += 1
        if all(lines[i - 1][jj] == 'S' for jj in (ptr - 1, ptr + 1)) \
                and all(lines[i + 1][jj] == 'M' for jj in (ptr - 1, ptr + 1)):
            count += 1
        if all(lines[ii][ptr - 1] == 'M' for ii in (i - 1, i + 1)) \
                and all(lines[ii][ptr + 1] == 'S' for ii in (i - 1, i + 1)):
            count += 1
        if all(lines[ii][ptr - 1] == 'S' for ii in (i - 1, i + 1)) \
                and all(lines[ii][ptr + 1] == 'M' for ii in (i - 1, i + 1)):
            count += 1
print(count)


