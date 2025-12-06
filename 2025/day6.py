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
    (sum if op == '+' else util.prod)(nlst)
    for nlst, op in zip(nums, ops)
))


# part 2
total = 0
numBuff = []
for l, op in zip(util.transpose(line for line in lines[:-1])[::-1], lines[-1][::-1]):
    line = ''.join(l).strip()
    if len(line) == 0:
        continue
    numBuff.append(int(line))
    if op != ' ':
        total += (sum if op == '+' else util.prod)(numBuff)
        numBuff.clear()
print(total)
