import AOCInit
import util
from operator import setitem

if __name__ != '__main__':
    exit()

inp = """\
#ip 0
seti 5 0 1
seti 6 0 2
addi 0 1 0
addr 1 2 3
setr 1 0 0
seti 8 0 4
seti 9 0 5\
"""
inp = util.getInput(d=19, y=2018)

reg = list(0 for _ in range(6))
commands = {
    'addr': (lambda cmd: setitem(reg, cmd[2], reg[cmd[0]] + reg[cmd[1]])),
    'addi': (lambda cmd: setitem(reg, cmd[2], reg[cmd[0]] + cmd[1])),
    'mulr': (lambda cmd: setitem(reg, cmd[2], reg[cmd[0]] * reg[cmd[1]])),
    'muli': (lambda cmd: setitem(reg, cmd[2], reg[cmd[0]] * cmd[1])),
    'banr': (lambda cmd: setitem(reg, cmd[2], reg[cmd[0]] & reg[cmd[1]])),
    'bani': (lambda cmd: setitem(reg, cmd[2], reg[cmd[0]] & cmd[1])),
    'borr': (lambda cmd: setitem(reg, cmd[2], reg[cmd[0]] | reg[cmd[1]])),
    'bori': (lambda cmd: setitem(reg, cmd[2], reg[cmd[0]] | cmd[1])),
    'setr': (lambda cmd: setitem(reg, cmd[2], reg[cmd[0]])),
    'seti': (lambda cmd: setitem(reg, cmd[2], cmd[0])),
    'gtir': (lambda cmd: setitem(reg, cmd[2], int(cmd[0] > reg[cmd[1]]))),
    'gtri': (lambda cmd: setitem(reg, cmd[2], int(reg[cmd[0]] > cmd[1]))),
    'gtrr': (lambda cmd: setitem(reg, cmd[2], int(reg[cmd[0]] > reg[cmd[1]]))),
    'eqir': (lambda cmd: setitem(reg, cmd[2], int(cmd[0] == reg[cmd[1]]))),
    'eqri': (lambda cmd: setitem(reg, cmd[2], int(reg[cmd[0]] == cmd[1]))),
    'eqrr': (lambda cmd: setitem(reg, cmd[2], int(reg[cmd[0]] == reg[cmd[1]]))),
}
ipSlot = int(inp.split('\n', maxsplit=1)[0][-1])
instructions = tuple((l.split(maxsplit=1)[0], util.getInts(l))
                     for l in inp.splitlines()[1:])
instructionCount = len(instructions)

# part 1

hitCount = list(0 for _ in range(instructionCount))
exeHistory = list()
while 0 <= reg[ipSlot] < instructionCount:
    hitCount[reg[ipSlot]] += 1
    exeHistory.append(reg[ipSlot])
    inst = instructions[reg[ipSlot]]
    commands[inst[0]](inst[1])
    reg[ipSlot] += 1
print(reg[0])

# part 2


