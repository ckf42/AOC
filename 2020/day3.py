import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=3, y=2020)
treeMap = inp.splitlines()
dim = (len(treeMap), len(treeMap[0]))

# part 1
def treesMet(k):
    return sum(treeMap[i][(k * i) % dim[1]] == '#' for i in range(dim[0]))

resDict: dict[int, int] = {3: treesMet(3)}
print(resDict[3])

# part 2
for i in (1, 5, 7):
    resDict[i] = treesMet(i)
print(util.prod(resDict.values()) \
        * sum(treeMap[i][(i // 2) % dim[1]] == '#'
              for i in range(0, dim[0], 2))
)
