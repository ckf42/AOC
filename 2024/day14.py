import AOCInit
import util
import time

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
def countConnected(gridmap):
    visited = set()
    counter = 0
    for i in range(w):
        for j in range(h):
            if not gridmap[i][j] or (i, j) in visited:
                continue
            counter += 1
            buff = [(i, j)]
            while len(buff) != 0:
                x, y = buff.pop()
                visited.add((x, y))
                for xx, yy in util.nearby2DGridPts((x, y), (w, h), False):
                    if gridmap[xx][yy] and (xx, yy) not in visited:
                        buff.append((xx, yy))
    return counter

jmpForward = 6000
n = len(robots)
locs = [
        [
            (bot[0] + jmpForward * bot[2]) % w,
            (bot[1] + jmpForward * bot[3]) % h
        ]
        for bot in robots
]
recs = []
for i in range(jmpForward + 1, 7000 + 1):
    grid = [[False] * h for _ in range(w)]
    for idx in range(n):
        locs[idx][0] = (locs[idx][0] + robots[idx][2]) % w
        locs[idx][1] = (locs[idx][1] + robots[idx][3]) % h
        grid[locs[idx][0]][locs[idx][1]] = True
    cc = countConnected(grid)
    if cc <= n // 3:
        recs.append('\n'.join(''.join((util.consoleChar(x) for x in r)) for r in util.transpose(grid)))
        print(i)
        print(recs[-1])
        print(('-' * 10 + '\n') * 3)
        time.sleep(0.20)

