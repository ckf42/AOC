import AOCInit
import util

from collections import defaultdict

if __name__ != '__main__':
    exit()

inp = util.getInput(d=8, y=2024)

nodeMap = inp.splitlines()
n = len(nodeMap)
m = len(nodeMap[0])

nodeDict = defaultdict(list)
for i in range(n):
    for j in range(m):
        if (c := nodeMap[i][j]) != '.':
            nodeDict[c].append((i, j))

# part 1
anodes = set()
for v in nodeDict.values():
    l = len(v)
    for i in range(l - 1):
        for j in range(i + 1, l):
            if (q1 := v[i][0] - v[j][0]) % 3 == 0 and (q2 := v[i][1] - v[j][1]) % 3 == 0:
                anodes.add((v[i][0] + q1 // 3, v[i][1] + q[1] // 3))
                anodes.add((v[j][0] - q1 // 3, v[j][1] - q[1] // 3))
            pt = (2 * v[i][0] - v[j][0], 2 * v[i][1] - v[j][1])
            if util.in2DRange(pt, n, m):
                anodes.add(pt)
            pt = (2 * v[j][0] - v[i][0], 2 * v[j][1] - v[i][1])
            if util.in2DRange(pt, n, m):
                anodes.add(pt)
print(len(anodes))

# part 2
anodes = set()
for v in nodeDict.values():
    l = len(v)
    for i in range(l - 1):
        for j in range(i + 1, l):
            delta = (v[j][0] - v[i][0], v[j][1] - v[i][1])
            g = util.gcd(*delta)
            if g == 0:
                g = max(delta)
            delta = (delta[0] // g, delta[1] // g)
            x, y = v[i]
            while True:
                if not util.in2DRange((x, y), n, m):
                    break
                anodes.add((x, y))
                x += delta[0]
                y += delta[1]
            x, y = v[i]
            while True:
                if not util.in2DRange((x, y), n, m):
                    break
                anodes.add((x, y))
                x -= delta[0]
                y -= delta[1]
print(len(anodes))


