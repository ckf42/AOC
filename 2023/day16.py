import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=16, y=2023)

layout = inp.splitlines()
dim = (len(layout), len(layout[0]))
reflectorDir = {
        '/': {(0, -1): (1, 0), (0, 1): (-1, 0), (-1, 0): (0, 1), (1, 0): (0, -1)},
        '\\': {(0, -1): (-1, 0), (0, 1): (1, 0), (-1, 0): (0, -1), (1, 0): (0, 1)}
}

# part 1
def findEnergized(initPos: tuple[int, int], initDir: tuple[int, int]):
    beamFront: list[tuple[tuple[int, int],
                          tuple[int, int]]] = [(initPos, initDir)]
    visited: set[tuple[tuple[int, int],
                       tuple[int, int]]] = set()
    while len(beamFront) != 0:
        pos, d = beamFront.pop()
        if not (0 <= pos[0] < dim[0] and 0 <= pos[1] < dim[1]) or (pos, d) in visited:
            continue
        visited.add((pos, d))
        c = layout[pos[0]][pos[1]]
        if c == '.' or (c == '-' and d[0] == 0) or (c == '|' and d[1] == 0):
            beamFront.append(((pos[0] + d[0], pos[1] + d[1]), d))
        elif c in '/\\':
            d = reflectorDir[c][d]
            beamFront.append(((pos[0] + d[0], pos[1] + d[1]), d))
        elif c == '-':
            for offset in (-1, 1):
                dd = (0, offset)
                beamFront.append(((pos[0] + dd[0], pos[1] + dd[1]), dd))
        else:
            for offset in (-1, 1):
                dd = (offset, 0)
                beamFront.append(((pos[0] + dd[0], pos[1] + dd[1]), dd))
    energized = frozenset(pos for pos, d in visited)
    return len(energized)

maxE = findEnergized((0, 0), (0, 1))
print(maxE)

# part 2
# TODO: takes ~4s, too slow
for i in range(dim[0]):
    maxE = max(findEnergized((i, 0), (0, 1)), maxE)
    maxE = max(findEnergized((i, dim[1] - 1), (0, -1)), maxE)
for j in range(dim[1]):
    maxE = max(findEnergized((0, j), (1, 0)), maxE)
    maxE = max(findEnergized((dim[0] - 1, j), (-1, 0)), maxE)
print(maxE)


