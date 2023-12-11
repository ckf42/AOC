import AOCInit
import util
from bisect import bisect

if __name__ != '__main__':
    exit()

inp = util.getInput(d=11, y=2023)

sky = inp.splitlines()
dim = (len(sky), len(sky[0]))
emptyRows = tuple(
        i
        for i in range(dim[0])
        if all(sky[i][j] == '.' for j in range(dim[1])))
emptyCols = tuple(
        j
        for j in range(dim[1])
        if all(sky[i][j] == '.' for i in range(dim[0])))
galaxies = tuple(
        divmod(i, dim[1] + 1)
        for i in util.rangeLen(inp)
        if inp[i] == '#')
emptyCoors = tuple(
        (bisect(emptyRows, g[0]), bisect(emptyCols, g[1]))
        for g in galaxies)

# part 1
def dist(i, j, weight=2):
    return abs(galaxies[i][0] - galaxies[j][0]) + abs(galaxies[i][1] - galaxies[j][1]) \
            + (abs(emptyCoors[i][0] - emptyCoors[j][0]) \
            + abs(emptyCoors[i][1] - emptyCoors[j][1])) * (weight - 1)

print(sum(dist(i, j)
          for i in range(len(galaxies))
          for j in range(i + 1, len(galaxies))))


# part 2
print(sum(dist(i, j, 1000000)
          for i in range(len(galaxies))
          for j in range(i + 1, len(galaxies))))


