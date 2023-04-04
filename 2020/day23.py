import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=23, y=2020)
moveCount = 100

initNumbers = tuple(map(lambda c: int(c) - 1, inp.strip())) # start with 0
cupCount = len(initNumbers)

assert set(initNumbers) == set(range(cupCount))
nextCup: list[int] = list(-1 for _ in initNumbers)
for i, c in enumerate(initNumbers):
    nextCup[c] = initNumbers[(i + 1) % cupCount]
assert all(c != -1 for c in nextCup)

# part 1
currCup = initNumbers[0]
buf: list[int] = list(-1 for _ in range(4))
for _ in range(moveCount):
    buf[0] = currCup
    buf[1] = nextCup[buf[0]]
    buf[2] = nextCup[buf[1]]
    buf[3] = nextCup[buf[2]]
    nextCup[currCup] = nextCup[buf[3]]
    destCup = (currCup - 1) if currCup != 0 else (cupCount - 1)
    while destCup in buf:
        destCup -= 1
        if destCup == -1:
            destCup = cupCount - 1
    # assert destCup is not None
    nextCup[buf[3]] = nextCup[destCup]
    nextCup[buf[2]] = buf[3]
    nextCup[buf[1]] = buf[2]
    nextCup[destCup] = buf[1]
    currCup = nextCup[currCup]
outBuffer: list[int] = [0]
while (n := nextCup[outBuffer[-1]]) != 0:
    outBuffer.append(n)
print(''.join(str(i + 1) for i in outBuffer[1:]))

# part 2
# ~15s
oneMill = 1000000
nextCup = list(-1 for _ in initNumbers)
for i, c in enumerate(initNumbers[:-1]):
    nextCup[c] = initNumbers[i + 1]
nextCup[initNumbers[-1]] = cupCount
nextCup.extend((i + 1 for i in range(cupCount, oneMill)))
nextCup[-1] = initNumbers[0]
cupCount = len(nextCup)

currCup = initNumbers[0]
buf = list(-1 for _ in range(4))
for _ in range(10 * oneMill):
    buf[0] = currCup
    buf[1] = nextCup[buf[0]]
    buf[2] = nextCup[buf[1]]
    buf[3] = nextCup[buf[2]]
    nextCup[currCup] = nextCup[buf[3]]
    destCup = (currCup - 1) if currCup != 0 else (cupCount - 1)
    while destCup in buf:
        destCup -= 1
        if destCup == -1:
            destCup = cupCount - 1
    # assert destCup is not None
    nextCup[buf[3]] = nextCup[destCup]
    nextCup[buf[2]] = buf[3]
    nextCup[buf[1]] = buf[2]
    nextCup[destCup] = buf[1]
    currCup = nextCup[currCup]
print((nextCup[0] + 1) * (nextCup[nextCup[0]] + 1))

