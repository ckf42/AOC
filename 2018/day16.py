import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=16, y=2018)

(knowledgeInp, testProg) = inp.split('\n' * 4)
codeSample = tuple(util.splitIntoGp(util.getInts(l), 4)
                  for l in knowledgeInp.split('\n' * 2))
commands = {
    'addr': (lambda cmd, reg: tuple(((reg[cmd[0]] + reg[cmd[1]]) if i == cmd[2] else reg[i])
                                    for i in range(4))),
    'addi': (lambda cmd, reg: tuple(((reg[cmd[0]] + cmd[1]) if i == cmd[2] else reg[i])
                                    for i in range(4))),
    'mulr': (lambda cmd, reg: tuple(((reg[cmd[0]] * reg[cmd[1]]) if i == cmd[2] else reg[i])
                                    for i in range(4))),
    'muli': (lambda cmd, reg: tuple(((reg[cmd[0]] * cmd[1]) if i == cmd[2] else reg[i])
                                    for i in range(4))),
    'banr': (lambda cmd, reg: tuple(((reg[cmd[0]] & reg[cmd[1]]) if i == cmd[2] else reg[i])
                                    for i in range(4))),
    'bani': (lambda cmd, reg: tuple(((reg[cmd[0]] & cmd[1]) if i == cmd[2] else reg[i])
                                    for i in range(4))),
    'borr': (lambda cmd, reg: tuple(((reg[cmd[0]] | reg[cmd[1]]) if i == cmd[2] else reg[i])
                                    for i in range(4))),
    'bori': (lambda cmd, reg: tuple(((reg[cmd[0]] | cmd[1]) if i == cmd[2] else reg[i])
                                    for i in range(4))),
    'setr': (lambda cmd, reg: tuple((reg[cmd[0]] if i == cmd[2] else reg[i])
                                    for i in range(4))),
    'seti': (lambda cmd, reg: tuple((cmd[0] if i == cmd[2] else reg[i])
                                    for i in range(4))),
    'gtir': (lambda cmd, reg: tuple((int(cmd[0] > reg[cmd[1]]) if i == cmd[2] else reg[i])
                                    for i in range(4))),
    'gtri': (lambda cmd, reg: tuple((int(reg[cmd[0]] > cmd[1]) if i == cmd[2] else reg[i])
                                    for i in range(4))),
    'gtrr': (lambda cmd, reg: tuple((int(reg[cmd[0]] > reg[cmd[1]]) if i == cmd[2] else reg[i])
                                    for i in range(4))),
    'eqir': (lambda cmd, reg: tuple((int(cmd[0] == reg[cmd[1]]) if i == cmd[2] else reg[i])
                                    for i in range(4))),
    'eqri': (lambda cmd, reg: tuple((int(reg[cmd[0]] == cmd[1]) if i == cmd[2] else reg[i])
                                    for i in range(4))),
    'eqrr': (lambda cmd, reg: tuple((int(reg[cmd[0]] == reg[cmd[1]]) if i == cmd[2] else reg[i])
                                    for i in range(4))),
}
possibleCor = {
    i: set(commands.keys())
    for i in range(16)
}

# part 1
opCounter = 0
for block in codeSample:
    fittingCode = 0
    for n, cb in commands.items():
        if block[2] == cb(block[1][1:], block[0]):
            fittingCode += 1
        else:
            possibleCor[block[1][0]].discard(n)
    if fittingCode >= 3:
        opCounter += 1
print(opCounter)

# part 2
confirmedCode = set()
hasCodePruned = True
while hasCodePruned:
    hasCodePruned = False
    for i in range(16):
        if i in confirmedCode:
            continue
        if len(possibleCor[i]) == 0:
            raise RuntimeError(f'{i} has no possible choice')
        elif len(possibleCor[i]) == 1:
            code = next(i for i in possibleCor[i])
            for j in range(16):
                if i != j:
                    possibleCor[j].discard(code)
            confirmedCode.add(i)
            hasCodePruned = True
assert all(len(v) == 1 for v in possibleCor.values())
codeCmdDict = {k: next(i for i in v) for k, v in possibleCor.items()}
register = (0, 0, 0, 0)
for cmd in util.splitIntoGp(util.getInts(testProg), 4):
    register = commands[codeCmdDict[cmd[0]]](cmd[1:], register)
print(register)


