import AOCInit
import util
from functools import cache

if __name__ != '__main__':
    exit()

inp = util.getInput(d=16, y=2023)

layout = inp.splitlines()
dim = (len(layout), len(layout[0]))

reflectorDir = {
    '/': {(0, 1): (-1, 0), (0, -1): (1, 0), (1, 0): (0, -1), (-1, 0): (0, 1)},
    '\\': {(0, 1): (1, 0), (0, -1): (-1, 0), (1, 0): (0, 1), (-1, 0): (0, -1)},
}

# part 1
# idea modified from
# https://old.reddit.com/r/adventofcode/comments/18jjpfk/2023_day_16_solutions/kdksx4i/
@cache
def unsplittedReach(
        initSplitter: tuple[int, int]
        ) -> tuple[set[tuple[int, int]], set[tuple[int, int]]]:
    """
    The reach from a splitter if the beam stops at splitters
    returns
    1. all tiles reached (including splitters)
    2. all splitter stopped at
    """
    visitedStates = set()
    visitedSplitter = set()
    stack = [(initSplitter, d)
             for d in (
                 ((1, 0), (-1, 0))
                 if layout[initSplitter[0]][initSplitter[1]] == '|'
                 else ((0, 1), (0, -1)))]
    while len(stack) != 0:
        pos, d = stack.pop()
        if not (0 <= pos[0] < dim[0] and 0 <= pos[1] < dim[1]) \
                or (pos, d) in visitedStates:
            continue
        visitedStates.add((pos, d))
        c = layout[pos[0]][pos[1]]
        if not ((c == '|' and d[0] == 0) or (c == '-' and d[1] == 0)):
            if c in '/\\':
                d = reflectorDir[c][d]
            stack.append(((pos[0] + d[0], pos[1] + d[1]), d))
        else:
            visitedSplitter.add(pos)
    return (set(pos for pos, d in visitedStates),
            visitedSplitter)

@cache
def splitterReach(initSplitter: tuple[int, int]) -> set[tuple[int, int]]:
    """
    return all tiles reached from a splitter
    """
    visited = set()
    reachedSplitters = set()
    stack = [initSplitter]
    while len(stack) != 0:
        splitter = stack.pop()
        if splitter in reachedSplitters:
            continue
        reachedSplitters.add(splitter)
        tiles, nextSplitters = unsplittedReach(splitter)
        visited.update(tiles)
        stack.extend(nextSplitters)
    return visited

def countTiles(pos: tuple[int, int], d: tuple[int, int]) -> int:
    """
    Assumed not start in between a loop
    """
    visited = set()
    while 0 <= pos[0] < dim[0] and 0 <= pos[1] < dim[1]:
        visited.add(pos)
        c = layout[pos[0]][pos[1]]
        if not ((c == '|' and d[0] == 0) or (c == '-' and d[1] == 0)):
            if c in '/\\':
                d = reflectorDir[c][d]
            pos = (pos[0] + d[0], pos[1] + d[1])
        else:
            visited.update(splitterReach(pos))
            break
    return len(visited)

print(countTiles((0, 0), (0, 1)))

# part 2
# would elim exit cells give better performance?
# this would require recording exits in above functions
maxE = 0
for i in range(dim[0]):
    maxE = max(maxE,
               countTiles((i, 0), (0, 1)),
               countTiles((i, dim[1] - 1), (0, -1)))
for j in range(dim[1]):
    maxE = max(maxE,
               countTiles((0, j), (1, 0)),
               countTiles((dim[0] - 1, j), (-1, 0)))
print(maxE)

