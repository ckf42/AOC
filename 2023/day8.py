import AOCInit
import util

from itertools import product
from math import ceil

# from sympy.ntheory.modular import solve_congruence


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
# LCM sol, idea from subreddit
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

# (slightly) more generic solution
# quite slow
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
#             pathStat.append((
#                 history[currPos],  # tail
#                 count - history[currPos],  # period
#                 zTime))  # when we hit Z
#             break
# # for each stat in pathStat,
# #     after stat[0] copies of inst,
# #     we enter a loop of length stat[1] copies of inst
# #     with stat[0] being the smallest of such property
# #     during the process, we hit Z at time stat[2]
# # this means that the (minimal) cycle is a factor of stat[1] * len(inst)
# # with stat[0], stat[1] can scale up len(inst) times on bad graphs
# assert all(len(stat[2]) != 0 for stat in pathStat),\
#     "Some pos never hit Z node"
# maxTails = max(stat[0] * len(inst) for stat in pathStat)
# assert all(maxTails <= zt for stat in pathStat for zt in stat[2]),\
#     "Hit Z before entering the loop. Case not implemented"
# # find x == tail * len(inst) + n * period * len(inst) + (zt - tail * len(inst))
# # equiv, x % (period * len(inst)) == -zt
# # on solve_congruence giving (offset, period),
# # step is min (offset + n * period) that is larger than maxTails
# periods = (stat[1] * len(inst) for stat in pathStat)
# ztCombs = (product(*(stat[2] for stat in pathStat)))
# print(min(ceil((maxTails - sol[0]) / sol[1]) * sol[1] + sol[0]
#           for zts in ztCombs
#           if (sol := solve_congruence(*(
#               (p, -zt)
#               for (p, zt) in zip(periods, zts))))))

