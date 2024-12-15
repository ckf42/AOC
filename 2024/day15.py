import AOCInit
import util

from collections import deque

if __name__ != '__main__':
    exit()

inp = util.getInput(d=15, y=2024)

warehouseLines = inp.split('\n\n')[0]
warehouse = list(list(r) for r in warehouseLines.splitlines())
n = len(warehouse)
m = len(warehouse[0])
inst = ''.join(r.strip() for r in inp.split('\n\n')[1])
dirs = {
        '^': (-1, 0),
        '>': (0, 1),
        'v': (1, 0),
        '<': (0, -1),
}

# part 1

x, y = divmod(warehouseLines.index('@'), m + 1)

for c in inst:
    d = dirs[c]
    moveStack = []
    xx, yy = x, y
    while True:
        if warehouse[xx][yy] == '.':
            break
        if warehouse[xx][yy] in '@O':
            moveStack.append((xx, yy))
            xx += d[0]
            yy += d[1]
        else:
            moveStack.clear()
            break
    while len(moveStack) != 0:
        pt = moveStack.pop()
        warehouse[xx][yy], warehouse[pt[0]][pt[1]] \
                = warehouse[pt[0]][pt[1]], warehouse[xx][yy]
        x, y = xx, yy
        xx, yy = pt
gpss = 0
for i in range(n):
    for j in range(m):
        if warehouse[i][j] == 'O':
            gpss += 100 * i + j
print(gpss)

# part 2
newWarehouse = list(
        list(
            x
            for c in r
            for x in {'#': '##', 'O': '[]', '.': '..', '@': '@.'}[c]
        )
        for r in warehouseLines.splitlines()
)
x, y = divmod(warehouseLines.index('@'), m + 1)
y *= 2
n = len(newWarehouse)
m *= 2
newWarehouse[x][y] = '.'

for c in inst:
    d = dirs[c]
    toMove = deque([(x, y)])
    moveBuff = []
    willMove = set()  # TODO: can we enum better to avoid this?
    while len(toMove) != 0:
        xx, yy = toMove.popleft()
        if (xx, yy) in willMove:
            continue
        willMove.add((xx, yy))
        newX, newY = xx + d[0], yy + d[1]
        moveBuff.append((xx, yy))
        obs = newWarehouse[newX][newY]
        if obs == '#':
            moveBuff.clear()
            break
        if obs == '.':
            continue
        if d[0] != 0:
            #vert
            oX, oY = newX, newY
            oY += 1 if obs == '[' else -1
            toMove.append((oX, oY))
        toMove.append((newX, newY))
    while len(moveBuff) != 0:
        xx, yy = moveBuff.pop()
        x = xx + d[0]
        y = yy + d[1]
        newWarehouse[xx][yy], newWarehouse[x][y] \
                = newWarehouse[x][y], newWarehouse[xx][yy]
gpss = 0
for i in range(n):
    for j in range(m):
        if newWarehouse[i][j] == '[':
            gpss += 100 * i + j
print(gpss)

