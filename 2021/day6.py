import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=6, y=2021)

initFishTimers = util.getInts(inp)
fishCount = list(0 for _ in range(9))
for t in initFishTimers:
    fishCount[t] += 1

# part 1
ptr = 0
for _ in range(80):
    fishCount[(ptr + 7) % 9] += fishCount[ptr]
    ptr = (ptr + 1) % 9
print(sum(fishCount))

# part 2
for _ in range(256 - 80):
    fishCount[(ptr + 7) % 9] += fishCount[ptr]
    ptr = (ptr + 1) % 9
print(sum(fishCount))

