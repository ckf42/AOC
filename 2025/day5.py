import AOCInit
import util

if __name__ != "__main__":
    exit()

inp = util.getInput(d=5, y=2025)

inp1, inp2 = inp.split("\n\n")
itvs = util.IntegerIntervals()
for line in inp1.splitlines():
    itvs.add(util.getInts(line, allowNegative=False))

# part 1
print(sum(x in itvs for x in util.getInts(inp2)))

# part 2
print(len(itvs))
