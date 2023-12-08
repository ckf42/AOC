import AOCInit
import util
from sympy.ntheory.modular import crt

if __name__ != '__main__':
    exit()

inp = util.getInput(d=8, y=2023)
inst = util.sub('LR', (0, 1), inp.split('\n\n')[0])
nodes = {
        linesplit[0]: (linesplit[2][1:-1], linesplit[3][:-1])
        for line in inp.split('\n\n')[1].splitlines()
        if (linesplit := line.split())}

# part 1
pos = 'AAA'
instPtr = 0
count = 0
while True:
    count += 1
    c = inst[instPtr]
    pos = nodes[pos][c]
    if pos == 'ZZZ':
        print(count)
        break
    instPtr = (instPtr + 1) % len(inst)


# part 2
# LCM sol
hitTimes = list()
for pos in (k for k in nodes.keys() if k[-1] == 'A'):
    currPos = pos
    count = 0
    instPtr = 0
    while True:
        count += 1
        c = inst[instPtr]
        currPos = nodes[currPos][c]
        if currPos[-1] == 'Z':
            hitTimes.append(count)
            break
        instPtr = (instPtr + 1) % len(inst)
print(util.lcm(*hitTimes))

# more generic solution?
# pathStat = list()
# for pos in (k for k in nodes.keys() if k[-1] == 'A'):
#     count = 0
#     currPos = pos
#     history = dict()
#     zTime = list()
#     while True:
#         history[currPos] = count
#         for i, c in enumerate(inst):
#             currPos = nodes[currPos][c]
#             if currPos[-1] == 'Z':
#                 zTime.append(count * len(inst) + i + 1)
#         count += 1
#         if currPos in history:
#             pathStat.append((count,  # period + tail
#                              history[currPos],  # tail
#                              zTime))  # when we hit Z
#             break
# # for each stat in pathStat,
# #     after stat[0] copies of inst,
# #     we end up at pos which we saw after some (stat[1]) whole copies of inst
# #     with stat[0] being the smallest of such property
# #     during the process, we hit Z at time stat[2]
# # this means that the cycle is a factor of (stat[0] - stat[1]) * len(inst)
# # with stat[0] can combinatorial blowup on bad graphs
# assert all(len(stat[2]) != 0 for stat in pathStat),\
#         "Some pos never hit Z"
# # the following happens to hold on (most?) input
# # and simiplifies the computation
# assert all(len(stat[2]) == 1 for stat in pathStat),\
#         "Some pos hit Z multiple times before looping"
# assert all(stat[2][0] % len(inst) == 0 for stat in pathStat)
