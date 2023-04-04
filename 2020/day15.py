import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=15, y=2020)
startingNumbers = util.getInts(inp)

# part 1
lastSpokenAt: dict[int, int] = dict()
for i, v in enumerate(startingNumbers[:-1]):
    lastSpokenAt[v] = i + 1
numbersSaid: set[int] = set(startingNumbers[:-1])
lastNumber = startingNumbers[-1]
for currTurn in range(len(startingNumbers) + 1, 2020 + 1):
    numberToSay = 0 if lastNumber not in numbersSaid else (currTurn - 1 - lastSpokenAt[lastNumber])
    numbersSaid.add(lastNumber)
    lastSpokenAt[lastNumber] = currTurn - 1
    lastNumber = numberToSay
print(lastNumber)

# part 2
# ~16s by ipython timeit
for currTurn in range(2020 + 1, 30000000 + 1):
    numberToSay = 0 if lastNumber not in numbersSaid else (currTurn - 1 - lastSpokenAt[lastNumber])
    numbersSaid.add(lastNumber)
    lastSpokenAt[lastNumber] = currTurn - 1
    lastNumber = numberToSay
print(lastNumber)

