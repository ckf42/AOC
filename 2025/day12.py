import AOCInit
import util

if __name__ != "__main__":
    exit()

inp = """\
0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2
"""

inp = util.getInput(d=12, y=2025)

shapeInp, regionInp = inp.rsplit("\n\n", maxsplit=1)
shapes = {
    util.getInts(part.split("\n", maxsplit=1)[0])[0]: part.split("\n", maxsplit=1)[1] for part in shapeInp.split("\n\n")
}
area = {i: sum(c == "#" for c in g) for i, g in shapes.items()}
regions = [
    ((nums[0], nums[1]), nums[2:]) for line in regionInp.splitlines() if (nums := util.getInts(line)) is not None
]


def rotate(isFillLst: tuple[bool, ...]) -> tuple[bool, ...]:
    return tuple(isFillLst[i] for i in [2, 5, 8, 1, 4, 7, 0, 3, 6])


def flipH(isFillLst: tuple[bool, ...]) -> tuple[bool, ...]:
    return tuple(isFillLst[i] for i in [6, 7, 8, 3, 4, 5, 0, 1, 2])


def flipV(isFillLst: tuple[bool, ...]) -> tuple[bool, ...]:
    return tuple(isFillLst[i] for i in [2, 1, 0, 5, 4, 3, 8, 7, 6])


shapePts = dict()
for idx, graph in shapes.items():
    r = tuple(c == "#" for c in "".join(graph.splitlines()))
    shapePts[idx] = set()
    for _ in range(4):
        r = rotate(r)
        shapePts[idx].add(r)
        shapePts[idx].add(flipH(r))
        shapePts[idx].add(flipV(r))
for k in shapePts:
    shapePts[k] = tuple(shapePts[k])


offset = [(i, j) for i in range(3) for j in range(3)]

# part 1
count = 0
for lidx, ((x, y), spec) in enumerate(regions):
    grid = [[False] * y for _ in range(x)]
    specExpanded = [idx for idx, count in enumerate(spec) for _ in range(count)]
    n = len(specExpanded)

    failedPlacements = set()

    def fill(idx, currPlacement: set) -> bool:
        if idx == n:
            return True
        currPlacementSerialized = tuple(sorted(currPlacement))
        if currPlacementSerialized in failedPlacements:
            return False
        shapeIdx = specExpanded[idx]
        for i in range(x - 2):
            for j in range(y - 2):
                for vidx, variant in enumerate(shapePts[shapeIdx]):
                    if not any(grid[i + offset[k][0]][j + offset[k][1]] for k in range(9) if variant[k]):
                        point = (i, j, shapeIdx, vidx)
                        for k in range(9):
                            if variant[k]:
                                grid[i + offset[k][0]][j + offset[k][1]] = True
                        currPlacement.add(point)
                        if fill(idx + 1, currPlacement):
                            return True
                        for k in range(9):
                            if variant[k]:
                                grid[i + offset[k][0]][j + offset[k][1]] = False
                        currPlacement.discard(point)
        failedPlacements.add(currPlacementSerialized)
        return False

    # print(lidx)
    if sum(area[gidx] for gidx in specExpanded) <= x * y and fill(0, set()):
        # print("filled")
        count += 1
    # else:
    #     print("fail")

print(count)


# part 2
# no part 2
