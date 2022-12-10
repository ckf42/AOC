import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=10, y=2022).splitlines()
regRec = [1, ]
crtQueue = list()

def draw(c):
    if abs(regRec[-1] - c) <= 1:
        crtQueue.append('#')
    else:
        crtQueue.append('.')
    return (0 if c >= 39 else c + 1)

currCol = 0
for inst in inp:
    currCol = draw(currCol)
    regRec.append(regRec[-1])
    if inst != 'noop':
        currCol = draw(currCol)
        regRec.append(regRec[-1] + int(inst.split(' ')[1]))

# part 1
print(sum(i * regRec[i - 1] for i in range(20, 221, 40)))

# part 2
for j in range(6):
    for i in range(40):
        print(crtQueue[i + j * 40], end='')
    print('')

