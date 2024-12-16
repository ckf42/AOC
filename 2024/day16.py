import AOCInit
import util

import heapq as hq
from collections import defaultdict

if __name__ != '__main__':
    exit()

inp = util.getInput(d=16, y=2024)

graph = inp.splitlines()
n = len(graph)
m = len(graph[0])
start = divmod(inp.index('S'), m + 1)
end = divmod(inp.index('E'), m + 1)
dirs = (
        (0, 1),
        (-1, 0),
        (0, -1),
        (1, 0)
)

# part 1

minCost = -1
visited: dict[tuple[int, int, int], int] = dict()
h = [(0, *start, 0, *start, 0)]
prevStates = defaultdict(set)
buff = []
while len(h) != 0:
    cost, x, y, d, ox, oy, od = hq.heappop(h)
    currState = (x, y, d)
    if visited.get((x, y, d), cost) == cost:
        prevStates[(x, y, d)].add((ox, oy, od))
    if (x, y) == end:
        if minCost == -1:
            print(cost)
            minCost = cost
        buff.append((x, y, d))
        continue
    if (x, y, d) in visited:
        continue
    if minCost != -1 and cost > minCost:
        break
    visited[(x, y, d)] = cost
    # r1
    newState = (x, y, (d + 1) % 4)
    if visited.get(newState, cost + 1000) == cost + 1000:
        hq.heappush(h, (cost + 1000, *newState, *currState))
    # r2
    newState = (x, y, (d + 3) % 4)
    if visited.get(newState, cost + 1000) == cost + 1000:
        hq.heappush(h, (cost + 1000, *newState, *currState))
    # f
    xx = x + dirs[d][0]
    yy = y + dirs[d][1]
    newState = (xx, yy, d)
    if graph[xx][yy] != '#' and visited.get(newState, cost + 1) == cost + 1:
        hq.heappush(h, (cost + 1, *newState, *currState))


# part 2
tiles = set()
while len(buff) != 0:
    x, y, d = buff.pop()
    tiles.add((x, y))
    if (x, y, d) != (*start, 0):
        buff.extend(prevStates[(x, y, d)])
print(len(tiles))

