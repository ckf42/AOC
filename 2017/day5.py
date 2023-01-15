import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=5, y=2017)

# part 1
pid = 0
jmpList = list(util.getInts(inp))
l = len(jmpList)
count = 0
while pid < l:
    jmpList[pid] += 1
    pid += jmpList[pid] - 1
    count += 1
print(count)

# part 2
# TODO: need to optimize. Currently takes ~12s
pid = 0
jmpList = list(util.getInts(inp))
count = 0
while pid < l:
    j = jmpList[pid]
    jmpList[pid] += 1 if j < 3 else -1
    pid += j
    count += 1
print(count)

