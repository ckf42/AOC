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
h = [(0, (*start, 0), 0)]
prevStates = defaultdict(set)
buff = []
while len(h) != 0:
    cost, currState, lastAction = hq.heappop(h)
    if visited.get(currState, cost) == cost:
        prevStates[currState].add(lastAction)
    if currState[:-1] == end:
        if minCost == -1:
            print(cost)
            minCost = cost
        buff.append(currState)
        continue
    if currState in visited:
        continue
    if minCost != -1 and cost > minCost:
        break
    visited[currState] = cost
    x, y, d = currState
    # r1
    newState = (x, y, (d + 1) % 4)
    if visited.get(newState, cost + 1000) == cost + 1000:
        hq.heappush(h, (cost + 1000, newState, 1))
    # r2
    newState = (x, y, (d + 3) % 4)
    if visited.get(newState, cost + 1000) == cost + 1000:
        hq.heappush(h, (cost + 1000, newState, 2))
    # f
    xx = x + dirs[d][0]
    yy = y + dirs[d][1]
    newState = (xx, yy, d)
    if graph[xx][yy] != '#' and visited.get(newState, cost + 1) == cost + 1:
        hq.heappush(h, (cost + 1, newState, 3))


# part 2
tiles = set()
added = set()
while len(buff) != 0:
    x, y, d = buff.pop()
    tiles.add((x, y))
    if (x, y, d) != (*start, 0) and (x, y, d) not in added:
        added.add((x, y, d))
        for lastAction in prevStates[(x, y, d)]:
            xx, yy, dd = x, y, d
            if lastAction == 1:
                dd = (d + 3) % 4
            elif lastAction == 2:
                dd = (d + 1) % 4
            elif lastAction == 3:
                xx -= dirs[d][0]
                yy -= dirs[d][1]
            buff.append((xx, yy, dd))
print(len(tiles))

