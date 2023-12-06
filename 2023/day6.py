import AOCInit
import util
import math

if __name__ != '__main__':
    exit()

inp = util.getInput(d=6, y=2023)

inpl = inp.splitlines()
games = tuple(zip(util.getInts(inpl[0]),
                  util.getInts(inpl[1])))

# part 1
def countWinWays(t, d):
    delta = t * t - 4 * d
    if delta < 0:
        return 0
    sqrtDelta = delta ** (1 / 2)
    maxHold = math.floor((t + sqrtDelta) / 2)
    # had to go PAST the line
    if (t - maxHold) * maxHold == d:
        maxHold -= 1
    minHold = math.ceil((t - sqrtDelta) / 2)
    if (t - minHold) * minHold == d:
        minHold += 1
    return maxHold - minHold + 1

print(util.prod(countWinWays(t, d) for (t, d) in games))

# part 2
newTime = int(''.join(str(t) for t in util.getInts(inpl[0])))
newDist = int(''.join(str(t) for t in util.getInts(inpl[1])))
print(countWinWays(newTime, newDist))

