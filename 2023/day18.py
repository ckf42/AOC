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
        'U': util.Point(-1, 0),
        'D': util.Point(1, 0),
        'L': util.Point(0, -1),
        'R': util.Point(0, 1),
}

pos = util.Point(0, 0)
circum = 0
corners = list()
for d, pathLen, _ in inst:
    corners.append(pos)
    pos += dirList[d] * pathLen
    circum += pathLen
assert pos == util.Point(0, 0)

print(int(util.polygonArea(corners)) + 1 + circum // 2)

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

pos = util.Point(0, 0)
circum = 0
corners = list()
for d, pathLen in newInst:
    pos += dirList[d] * pathLen
    corners.append(pos)
    circum += pathLen
assert pos == util.Point(0, 0)

print(int(util.polygonArea(corners)) + 1 + circum // 2)

