import AOCInit
import util
import heapq as hq

# TODO: speed up. Currently takes ~4s for both parts

if __name__ != '__main__':
    exit()

inp = util.getInput(d=17, y=2023)

heatmap = tuple(tuple(int(c) for c in line)
                for line in inp.splitlines())
dim = (len(heatmap), len(heatmap[0]))
dirList = ((1, 0), (0, 1), (0, -1), (-1, 0))

# part 1
def minLoss(maxStep, minStep=1):
    visited = set()
    h = [(0, (0, 0), -1)]  # cost, pos, prev dir idx
    while len(h) != 0:
        cost, pos, prevDIdx = hq.heappop(h)
        if (pos, prevDIdx) in visited:
            continue
        if pos == (dim[0] - 1, dim[1] - 1):
            return cost
        visited.add((pos, prevDIdx))
        for dIdx in range(4):
            if dIdx in (prevDIdx, 3 - prevDIdx):
                continue
            d = dirList[dIdx]
            newCost = cost
            newPos = pos
            for step in range(1, maxStep + 1):
                newPos = (newPos[0] + d[0], newPos[1] + d[1])
                if not (0 <= newPos[0] < dim[0] and 0 <= newPos[1] < dim[1]):
                    break
                newCost += heatmap[newPos[0]][newPos[1]]
                if step >= minStep and (newPos, dIdx) not in visited:
                    hq.heappush(h, (newCost, newPos, dIdx))

print(minLoss(maxStep=3))

# part 2
print(minLoss(maxStep=10, minStep=4))
