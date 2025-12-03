import AOCInit
import util

if __name__ != "__main__":
    exit()

inp = util.getInput(d=3, y=2025)

# part 1
total = 0
for line in inp.splitlines():
    l = len(line)
    maxAfter = [0] * l
    opt = 0
    for i in range(l - 2, -1, -1):
        maxAfter[i] = max(maxAfter[i + 1], int(line[i + 1]))
        opt = max(opt, int(line[i]) * 10 + maxAfter[i])
    total += opt
print(total)

# part 2
total = 0
for line in inp.splitlines():
    maxVal = [0] * (12 + 1)
    for x in (int(c) for c in line):
        for l in range(12, 0, -1):
            maxVal[l] = max(maxVal[l], maxVal[l - 1] * 10 + x)
    total += maxVal[12]
print(total)

