import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=7, y=2024)

nums = tuple(
        util.getInts(line)
        for line in inp.splitlines()
)

# part 1
evalState = [False] * len(nums)
total = 0
for i, rec in enumerate(nums):
    buff = set((rec[0],))
    for x in rec[-1:1:-1]:
        newBuff = set()
        for y in buff:
            if y >= x:
                newBuff.add(y - x)
            if y % x == 0:
                newBuff.add(y // x)
        buff = newBuff
    if rec[1] in buff:
        total += rec[0]
        evalState[i] = True
print(total)


# part 2
for i, rec in enumerate(nums):
    if evalState[i]:
        continue
    buff = set((rec[0],))
    for x in rec[-1:1:-1]:
        newBuff = set()
        for y in buff:
            if y >= x:
                newBuff.add(y - x)
            if y % x == 0:
                newBuff.add(y // x)
            strx = str(x)
            stry = str(y)
            if len(strx) < len(stry) and stry.endswith(strx):
                newBuff.add(int(stry[:-len(strx)]))
        buff = newBuff
    if rec[1] in buff:
        total += rec[0]
print(total)


