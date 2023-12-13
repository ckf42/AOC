import AOCInit
import util
from bisect import bisect

if __name__ != '__main__':
    exit()

inp = util.getInput(d=11, y=2023)
# updated to work on more complicated input
# from https://old.reddit.com/r/adventofcode/comments/18h1hho/2023_day_11_a_more_challenging_input_complexity/
# inp = ''
# with open('test11.txt', 'rt') as f:
#     inp = f.read()

sky = inp.splitlines()
dim = (len(sky), len(sky[0]))

# can we optimize this from 3 passes to 1 pass?
emptyRows = tuple(
        i
        for i in range(dim[0])
        if all(sky[i][j] == '.' for j in range(dim[1])))
emptyCols = tuple(
        j
        for j in range(dim[1])
        if all(sky[i][j] == '.' for i in range(dim[0])))
galaxyX = list()
galaxyY = list()
for i in range(dim[0]):
    for j in range(dim[1]):
        if sky[i][j] == '#':
            galaxyX.append(i)
            galaxyY.append(j)

galaxyY.sort()  # only y is not inserted in order

# this can be further optimized
# by replacing bisect (n log n) with rolling (n)
emptyX = tuple(bisect(emptyRows, x) for x in galaxyX)
emptyY = tuple(bisect(emptyCols, y) for y in galaxyY)

normalDist = sum((x + y) * (2 * i - len(galaxyX) + 1)
                 for i, (x, y) in enumerate(zip(galaxyX, galaxyY)))
expandDist = sum((x + y) * (2 * i - len(emptyX) + 1)
                 for i, (x, y) in enumerate(zip(emptyX, emptyY)))

# part 1
print(normalDist + expandDist)

# part 2
print(normalDist + expandDist * (1000000 - 1))

