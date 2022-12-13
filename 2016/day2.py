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
        loc = tuple(util.clip(loc[i] + d[i], 0, 2) for i in range(2))
    codeBuffer.append(str(1 + loc[0] + loc[1] * 3))
print(''.join(codeBuffer))

# part 2
keypad = util.splitIntoGp([0, 0, 1, 0, 0,
                           0, 2, 3, 4, 0,
                           5, 6, 7, 8, 9,
                           0, 10, 11, 12, 0,
                           0, 0, 13, 0, 0], 5)
keypad = util.transpose(keypad)
codeBuffer = list()
loc = (2, 2)
for line in inp:
    for c in line:
        d = moveDict[c]
        newLoc = tuple(util.clip(loc[i] + d[i], 0, 4) for i in range(2))
        if keypad[newLoc[0]][newLoc[1]] != 0:
            loc = newLoc
    codeBuffer.append(hex(keypad[loc[0]][loc[1]])[2:].upper())
print(''.join(codeBuffer))

