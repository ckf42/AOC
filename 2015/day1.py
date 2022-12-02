import AOCInit
import util

inp = util.getInput(d=1, y=2015)

# part 1
print(sum((1 if c == '(' else -1) for c in inp))

# part 2
ind = 0
currentFloor = 0
while ind < len(inp) and currentFloor >= 0:
    currentFloor += (1 if inp[ind] == '(' else -1)
    ind += 1
print(ind)
