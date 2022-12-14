import AOCInit
import util
import numpy as np

if __name__ != '__main__':
    exit()

inp = tuple(l.split() for l in util.getInput(d=8, y=2016).splitlines())
lcdDim = (6, 50)
lcd = np.zeros(lcdDim, dtype=bool)

def printLCD():
    for r in range(lcdDim[0]):
        for c in range(lcdDim[1]):
            print(util.consoleChar(lcd[r, c]), end='')
        print('')

# part 1
for inst in inp:
    if inst[0] == 'rect':
        s = util.getInts(inst[1])
        lcd[:s[1], :s[0]] = True
    elif inst[1] == 'row':
        r = int(inst[2][2:])
        offset = int(inst[4])
        lcd[r, :] = lcd[r, np.r_[-offset:lcdDim[1]-offset]]
    else:
        c = int(inst[2][2:])
        offset = int(inst[4])
        lcd[:, c] = lcd[np.r_[-offset:lcdDim[0]-offset], c]
print(np.sum(lcd))

# part 2
printLCD()

