import AOCInit
import util

if __name__ != '__main__':
    exit()


inp = util.getInput(d=12, y=2024)

garden = inp.splitlines()
n = len(garden)
m = len(garden[0])


# part 1
visited = set()

area = []
peri = []
sides: list[set[tuple[int, int, bool, bool]]] = []

for i in range(n):
    for j in range(m):
        if (i, j) in visited:
            continue
        buff = [(i, j)]
        c = garden[i][j]
        a = 0
        p = 0
        sideEdges = set()
        while len(buff) != 0:
            x, y = buff.pop()
            if (x, y) in visited:
                continue
            visited.add((x, y))
            a += 1
            p += 4
            for dx, dy in util.integerLattice(2, 1, 1):
                xx = x + dx
                yy = y + dy
                if util.in2DRange((xx, yy), n, m) and garden[xx][yy] == c:
                    p -= 1
                    if (xx, yy) not in visited:
                        buff.append((xx, yy))
                else:
                    match (dx, dy):
                        case (-1, 0):
                            sideEdges.add((x, y, True, True))
                        case (0, -1):
                            sideEdges.add((x, y, False, True))
                        case (1, 0):
                            sideEdges.add((x + 1, y, True, False))
                        case (0, 1):
                            sideEdges.add((x, y + 1, False, False))
        area.append(a)
        peri.append(p)
        sides.append(sideEdges)
print(sum(a * p for a, p in zip(area, peri)))

# part 2
sideCount: list[int] = []
for edges in sides:
    count = 0
    while len(edges) != 0:
        x, y, isTopEdge, isSameDir = edges.pop()
        count += 1
        if isTopEdge:
            for yy in range(y - 1, -1, -1):
                if (e := (x, yy, True, isSameDir)) not in edges:
                    break
                edges.remove(e)
            for yy in range(y + 1, m + 1):
                if (e := (x, yy, True, isSameDir)) not in edges:
                    break
                edges.remove(e)
        else:
            for xx in range(x - 1, -1, -1):
                if (e := (xx, y, False, isSameDir)) not in edges:
                    break
                edges.remove(e)
            for xx in range(x + 1, n + 1):
                if (e := (xx, y, False, isSameDir)) not in edges:
                    break
                edges.remove(e)
    sideCount.append(count)
print(sum(a * s for a, s in zip(area, sideCount)))


