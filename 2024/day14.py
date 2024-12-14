import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=14, y=2024)
w, h = 101, 103
t = 100

robots = tuple(
        util.getInts(line)
        for line in inp.splitlines()
)

# part 1
quadCount = [0] * 4
for bot in robots:
    x = (bot[0] + bot[2] * t) % w
    if x == w // 2:
        continue
    y = (bot[1] + bot[3] * t) % h
    if y == h // 2:
        continue
    quadCount[(x < w // 2) + 2 * (y < h // 2)] += 1
print(util.prod(quadCount))



# part 2
n = len(robots)
locs = [
        list(bot[:2])
        for bot in robots
]
ratios = []
sampleN = 100
for i in range(1, sampleN + 1):
    grid = [[False] * h for _ in range(w)]
    for idx in range(n):
        locs[idx][0] = (locs[idx][0] + robots[idx][2]) % w
        locs[idx][1] = (locs[idx][1] + robots[idx][3]) % h
        grid[locs[idx][0]][locs[idx][1]] = True
    consoleStr = '\n'.join(''.join(util.consoleChar(x) for x in r) for r in util.transpose(grid))
    ratios.append(util.compressionRatio(consoleStr))
mean = sum(ratios) / sampleN
secondMoment = sum(x ** 2 for x in ratios) / sampleN
for i in range(sampleN + 1, 10000 + 1):
    grid = [[False] * h for _ in range(w)]
    for idx in range(n):
        locs[idx][0] = (locs[idx][0] + robots[idx][2]) % w
        locs[idx][1] = (locs[idx][1] + robots[idx][3]) % h
        grid[locs[idx][0]][locs[idx][1]] = True
    consoleStr = '\n'.join(''.join(util.consoleChar(x) for x in r) for r in util.transpose(grid))
    r = util.compressionRatio(consoleStr)
    if r > mean + (secondMoment - mean ** 2) ** 0.5 * 10:
        print(consoleStr)
        print(i)
        break
    mean = (mean * (i - 1) + r) / i
    secondMoment = (secondMoment * (i - 1) + r ** 2) / i

