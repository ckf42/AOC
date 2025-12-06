import AOCInit
import util

if __name__ != '__main__':
    exit()


inp = util.getInput(d=6, y=2025)

lines = inp.splitlines()

# part 1
nums = util.transpose(util.getInts(l) for l in lines[:-1])
ops = lines[-1].split()
print(sum(
    sum(nlst) if op == '+' else util.prod(nlst)
    for nlst, op in zip(nums, ops)
))


# part 2
l = len(lines) - 1
total = 0
prevOp = ' '
numBuff = []
for j, c in enumerate(lines[-1]):
    x = 0
    isBlank = True
    for i in range(0, l):
        if lines[i][j] != ' ':
            x = 10 * x + int(lines[i][j])
            isBlank = False
    if isBlank:
        total += sum(numBuff) if prevOp == '+' else util.prod(numBuff)
        numBuff.clear()
    else:
        numBuff.append(x)
    if c != ' ':
        prevOp = c
total += sum(numBuff) if prevOp == '+' else util.prod(numBuff)
print(total)

