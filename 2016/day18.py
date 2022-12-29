import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=18, y=2016).strip()

inp = util.sub('^.', (True, False), inp)
l = len(inp)

# part 1
rowCount = 40
buff = inp
safeCount = util.countItem(buff, False)
for i in range(rowCount - 1):
    buff = (buff[1],) + tuple(buff[i - 1] ^ buff[i + 1] for i in range(1, l - 1)) + (buff[-2],)
    safeCount += util.countItem(buff, False)
print(safeCount)


# part 2
rowCount = 400000
buff = inp
safeCount = util.countItem(buff, False)
for i in range(rowCount - 1):
    buff = (buff[1],) + tuple(buff[i - 1] ^ buff[i + 1] for i in range(1, l - 1)) + (buff[-2],)
    safeCount += util.countItem(buff, False)
print(safeCount)

