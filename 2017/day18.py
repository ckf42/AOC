import AOCInit
import util
from collections import deque

if __name__ != '__main__':
    exit()

inp = """\
set a 1
add a 2
mul a a
mod a 5
snd a
set a 0
rcv a
jgz a -1
set a 1
jgz a -2\
"""
inp = util.getInput(d=18, y=2017)

instList = {
    i: tuple((int(t) if t[-1].isdigit() else t) for t in l.split())
    for i, l in enumerate(inp.splitlines())
}
l = len(instList)

# part 1
register: dict[str, int] = {chr(ord('a') + i): 0 for i in range(26)}
lastPlayedFreq = None
pid = 0
while pid < l:
    pidOffset = 1
    inst = instList[pid]
    if inst[0] == 'snd':
        lastPlayedFreq = register.get(inst[1], inst[1])
    elif inst[0] == 'set':
        register[inst[1]] = register.get(inst[2], inst[2])
    elif inst[0] == 'add':
        register[inst[1]] += register.get(inst[2], inst[2])
    elif inst[0] == 'mul':
        register[inst[1]] *= register.get(inst[2], inst[2])
    elif inst[0] == 'mod':
        register[inst[1]] %= register.get(inst[2], inst[2])
    elif inst[0] == 'rcv':
        if register.get(inst[1], inst[1]) != 0:
            break
    elif inst[0] == 'jgz':
        if register.get(inst[1], inst[1]) > 0:
            pidOffset = register.get(inst[2], inst[2])
    pid += pidOffset
print(lastPlayedFreq)

# part 2
pgRegister: list[dict[str, int]] = [{chr(ord('a') + i): 0 for i in range(26)} for _ in range(2)]
for i in range(2):
    pgRegister[i]['p'] = i
pgPid: list[int] = [0, 0]
recvQ: list[deque[int]] = [deque(), deque()]
pgStatus: list[int] = [0, 0] # 0: running, 1: waiting, 2: terminated
currPg: int = 0
sentCount = 0
while True:
    # check if currPg can be run
    if pgStatus[currPg] == 2 \
            or (pgStatus[currPg] == 1 and len(recvQ[currPg]) == 0):
        # attempt to resume a program that should not be run
        break
    # run pg
    while pgPid[currPg] < l:
        pidOffset = 1
        inst = instList[pgPid[currPg]]
        if inst[0] == 'snd':
            recvQ[1 - currPg].append(pgRegister[currPg].get(inst[1], inst[1]))
            if currPg == 1:
                sentCount += 1
        elif inst[0] == 'set':
            pgRegister[currPg][inst[1]] = pgRegister[currPg].get(inst[2], inst[2])
        elif inst[0] == 'add':
            pgRegister[currPg][inst[1]] += pgRegister[currPg].get(inst[2], inst[2])
        elif inst[0] == 'mul':
            pgRegister[currPg][inst[1]] *= pgRegister[currPg].get(inst[2], inst[2])
        elif inst[0] == 'mod':
            pgRegister[currPg][inst[1]] %= pgRegister[currPg].get(inst[2], inst[2])
        elif inst[0] == 'rcv':
            if len(recvQ[currPg]) != 0:
                pgRegister[currPg][inst[1]] = recvQ[currPg].popleft()
            else:
                pgStatus[currPg] = 1
                break
        elif inst[0] == 'jgz':
            if pgRegister[currPg].get(inst[1], inst[1]) > 0:
                pidOffset = pgRegister[currPg].get(inst[2], inst[2])
        pgPid[currPg] += pidOffset
    if pgPid[currPg] >= l:
        pgStatus[currPg] = 2
    # need to switch pg
    currPg = 1 - currPg
print(sentCount)

