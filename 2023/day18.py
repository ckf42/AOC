import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=18, y=2023)

# part 1
inst = tuple((ls[0], int(ls[1]), ls[2][2:-1])
             for line in inp.splitlines()
             if (ls := line.split()))
dirList = {
        'U': (-1, 0),
        'D': (1, 0),
        'L': (0, -1),
        'R': (0, 1),
}

pos = (0, 0)
circum = 0
corners = list()
for d, pathLen, _ in inst:
    dd = dirList[d]
    pos = (pos[0] + pathLen * dd[0], pos[1] + pathLen * dd[1])
    corners.append(pos)
    circum += pathLen
assert pos == (0, 0)

doubleArea = 0
for i in range(-1, len(corners) - 1):
    doubleArea += corners[i][0] * corners[i + 1][1] - corners[i][1] * corners[i + 1][0]
print((abs(doubleArea) - circum) // 2 + 1 + circum)

# part 2
digitDict = {
        '0': 'R',
        '1': 'D',
        '2': 'L',
        '3': 'U',
}
newInst = tuple(
        (digitDict[line[2][-1]], int(line[2][:-1], base=16))
        for line in inst)

pos = (0, 0)
circum = 0
corners = list()
for d, pathLen in newInst:
    dd = dirList[d]
    pos = (pos[0] + pathLen * dd[0], pos[1] + pathLen * dd[1])
    corners.append(pos)
    circum += pathLen
assert pos == (0, 0)

doubleArea = 0
for i in range(-1, len(corners) - 1):
    doubleArea += corners[i][0] * corners[i + 1][1] - corners[i][1] * corners[i + 1][0]
print((abs(doubleArea) - circum) // 2 + 1 + circum)

