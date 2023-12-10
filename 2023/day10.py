import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=10, y=2023)

ground = inp.splitlines()
dim = (len(ground), len(ground[0]))
sPos = divmod(inp.index('S'), dim[1] + 1)
pipeSyms = '|-LJ7F'

def nbPos(pos, asSym=None):
    sym = ground[pos[0]][pos[1]] if asSym is None else asSym
    if sym == '|':
        dirs = ((1, 0), (-1, 0))
    elif sym == '-':
        dirs = ((0, 1), (0, -1))
    elif sym == 'L':
        dirs = ((-1, 0), (0, 1))
    elif sym == 'J':
        dirs = ((-1, 0), (0, -1))
    elif sym == '7':
        dirs = ((1, 0), (0, -1))
    elif sym == 'F':
        dirs = ((1, 0), (0, 1))
    else:
        return tuple()
    return tuple((pos[0] + i, pos[1] + j) for (i, j) in dirs)

# part 1
possibleEnds = list()
for nb in util.nearby2DGridPts(sPos, dim):
    if sPos in nbPos(nb):
        possibleEnds.append((nb, sPos))
visited = {sPos: (0, sPos)}  # (dist, prev pos)
furthestPt = None
corrDir: list[tuple[int, int]] | None = None
while True:
    newEnds = list()
    found = False
    for pos, prevPos in possibleEnds:
        for newPos in nbPos(pos):
            if newPos == prevPos or pos not in nbPos(newPos):
                continue
            if pos in visited:
                found = True
                furthestPt = pos
                corrDir = sorted((visited[pos][1], visited[prevPos][1]))
                print(visited[pos][0])
                break
            else:
                newEnds.append((newPos, pos))
                vp = visited[prevPos]
                visited[pos] = (vp[0] + 1, vp[1] if vp[1] != sPos else prevPos)
    if found:
        break
    possibleEnds = newEnds
assert corrDir is not None

# part 2
def isBdy(pos):
    return pos == sPos \
            or pos in corrDir \
            or visited.get(pos, (None, None))[1] in corrDir

sSym = util.firstSuchThat(
        pipeSyms,
        lambda sym: sorted(nbPos(sPos, sym)) == corrDir)[1]
assert sSym is not None
totalArea = 0
for r in range(dim[0]):
    isInside = False
    for c in range(dim[1]):
        sym = ground[r][c] if (r, c) != sPos else sSym
        if not isBdy((r, c)):
            # assert upIsInside == downIsInside, "This is not supposed to happen"
            # here we assumed that the above assert must hold
            # when upIsInside and downIsInside are maintained
            # (which is the case except on defected graph?)
            if isInside:
                totalArea += 1
        elif sym in '|LJ':
            isInside = not isInside
print(totalArea)

