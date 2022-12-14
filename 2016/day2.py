import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=2, y=2016).splitlines()

# part 1
moveDict = {'U': (0, -1), 'D': (0, 1), 'L': (-1, 0), 'R': (1, 0)}
codeBuffer = list()
loc = (1, 1)
for line in inp:
    for c in line:
        d = moveDict[c]
        newLoc = tuple(loc[i] + d[i] for i in range(2))
        if max(abs(newLoc[i] - 1) for i in range(2)) <= 1:
            loc = newLoc
    codeBuffer.append(str(1 + loc[0] + loc[1] * 3))
print(''.join(codeBuffer))

# part 2
codeBuffer = list()
loc = (0, 0)
for line in inp:
    for c in line:
        d = moveDict[c]
        newLoc = tuple(loc[i] + d[i] for i in range(2))
        if sum(abs(newLoc[i]) for i in range(2)) <= 2:
            loc = newLoc
    codeBuffer.append(hex(7 + loc[0] + util.cycInd((0, 4, 6, -6, -4), loc[1]))[2:].upper())
print(''.join(codeBuffer))

