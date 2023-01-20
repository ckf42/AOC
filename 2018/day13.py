import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=13, y=2018)

railMap = inp.splitlines()
dim = (len(railMap), len(railMap[0]))
cartLoc = [complex(*divmod(i, dim[1] + 1)) for i in range(len(inp)) if inp[i] in '<^v>']
cartCount = len(cartLoc)
directions = (-1, 1j, 1, -1j)
cartDir = ['^>v<'.index(railMap[int(pt.real)][int(pt.imag)]) for pt in cartLoc]
turnOffset = [-1 for _ in cartDir] # -1, 0, 1
cartOrderBuff: tuple[util.Heap, util.Heap] = (
        util.MinHeap(tuple(enumerate(cartLoc)), lambda pr: (pr[1].imag, pr[1].real)),
        util.MinHeap(key=lambda pr: (pr[1].imag, pr[1].real)))
buffPtr = 0

# part 1
collisionLoc = None
while True:
    cartOrderBuff[1 - buffPtr].clear()
    while not cartOrderBuff[buffPtr].isEmpty():
        cartToMove = cartOrderBuff[buffPtr].pop()[0]
        (x, y) = (int(cartLoc[cartToMove].real), int(cartLoc[cartToMove].imag))
        if railMap[x][y] == '+':
            cartDir[cartToMove] = (cartDir[cartToMove] + turnOffset[cartToMove]) % 4
            turnOffset[cartToMove] = (turnOffset[cartToMove] + 2) % 3 - 1
        elif railMap[x][y] in r'\/':
            cartDir[cartToMove] = (cartDir[cartToMove] \
                    + (-1
                    if (cartDir[cartToMove] + r'\/'.index(railMap[x][y])) % 2 == 0
                    else 1)) % 4
        newLoc = cartLoc[cartToMove] + directions[cartDir[cartToMove]]
        if newLoc in cartLoc:
            collisionLoc = newLoc
            break
        else:
            cartLoc[cartToMove] = newLoc
            cartOrderBuff[1 - buffPtr].push((cartToMove, newLoc))
    if collisionLoc is not None:
        break
    buffPtr = 1 - buffPtr
print(f'{int(collisionLoc.imag)},{int(collisionLoc.real)}')

# part 2
cartLoc = [complex(*divmod(i, dim[1] + 1)) for i in range(len(inp)) if inp[i] in '<^v>']
cartDir = ['^>v<'.index(railMap[int(pt.real)][int(pt.imag)]) for pt in cartLoc]
turnOffset = [-1 for _ in cartDir] # -1, 0, 1
for i in range(2):
    cartOrderBuff[i].clear()
cartOrderBuff[0].extend(tuple(enumerate(cartLoc)))
buffPtr = 0
remainCartCount = cartCount
while remainCartCount > 1:
    cartOrderBuff[1 - buffPtr].clear()
    while not cartOrderBuff[buffPtr].isEmpty():
        cartToMove = cartOrderBuff[buffPtr].pop()[0]
        (x, y) = (int(cartLoc[cartToMove].real), int(cartLoc[cartToMove].imag))
        if railMap[x][y] == '+':
            cartDir[cartToMove] = (cartDir[cartToMove] + turnOffset[cartToMove]) % 4
            turnOffset[cartToMove] = (turnOffset[cartToMove] + 2) % 3 - 1
        elif railMap[x][y] in r'\/':
            cartDir[cartToMove] = (cartDir[cartToMove] \
                    + (-1
                    if (cartDir[cartToMove] + r'\/'.index(railMap[x][y])) % 2 == 0
                    else 1)) % 4
        newLoc = cartLoc[cartToMove] + directions[cartDir[cartToMove]]
        if newLoc in cartLoc:
            hitIdx = cartLoc.index(newLoc)
            for i in range(2):
                cartOrderBuff[i].discard((hitIdx, newLoc))
                cartOrderBuff[i].discard((cartToMove, newLoc))
            cartLoc[hitIdx] = None
            cartLoc[cartToMove] = None
            remainCartCount -= 2
        else:
            cartLoc[cartToMove] = newLoc
            cartOrderBuff[1 - buffPtr].push((cartToMove, newLoc))
    buffPtr = 1 - buffPtr
collisionLoc = cartOrderBuff[buffPtr].top()[1]
print(f'{int(collisionLoc.imag)},{int(collisionLoc.real)}')


