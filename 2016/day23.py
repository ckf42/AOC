import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = """\
cpy 2 a
tgl a
tgl a
tgl a
cpy 1 a
dec a
dec a\
"""
inp = util.getInput(d=23, y=2016)

# part 1
instDict = {i: tuple((int(term) if term[-1].isdigit() else term)
                     for term in l.split())
            for i, l in enumerate(inp.splitlines())}
l = len(instDict)

def optimizedInst(origInstDict: dict):
    newInstDict = origInstDict.copy()
    for i in range(1, l - 1):
        if newInstDict[i][0] == 'dec' \
                and newInstDict[i + 1] == ('jnz', newInstDict[i][1], -2) \
                and newInstDict[i - 1][0] in ('inc', 'dec') \
                and newInstDict[i - 1][1] != newInstDict[i][1]:
            newInstDict[i - 1] = (
                    '+=' if newInstDict[i - 1][0] == 'inc' else '-=',
                    newInstDict[i - 1][1],
                    newInstDict[i][1]
            )
            newInstDict[i] = newInstDict[i + 1] = ('nop',)
    return newInstDict

def executeInst(register):
    unoptInstDict = instDict.copy()
    currInstDict = optimizedInst(unoptInstDict)
    pid = 0
    while pid < l:
        inst = currInstDict[pid]
        pidOffset = 1
        if inst[0] == 'nop':
            pass
        elif inst[0] == 'cpy':
            register[inst[2]] = register.get(inst[1], inst[1])
        elif inst[0] == 'inc':
            register[inst[1]] += 1
        elif inst[0] == 'dec':
            register[inst[1]] -= 1
        elif inst[0] == 'jnz':
            if register.get(inst[1], inst[1]) != 0:
                pidOffset = register.get(inst[2], inst[2])
                assert instDict[pid + pidOffset][0] != 'nop'
        elif inst[0] == '+=':
            register[inst[1]] += register.get(inst[2], inst[2])
        elif inst[0] == '-=':
            register[inst[1]] -= register.get(inst[2], inst[2])
        elif inst[0] == 'tgl' \
                and 0 <= (tPid := pid + register.get(inst[1], inst[1])) < l:
            if len(unoptInstDict[tPid]) == 2:
                if isinstance(unoptInstDict[tPid][1], int):
                    unoptInstDict[tPid] = ('nop',)
                else:
                    unoptInstDict[tPid] = (
                            'dec' if unoptInstDict[tPid][0] == 'inc' else 'inc',
                            unoptInstDict[tPid][1])
            else:
                unoptInstDict[tPid] = (
                        'cpy' if unoptInstDict[tPid][0] == 'jnz' else 'jnz',) \
                                + unoptInstDict[tPid][1:]
                if unoptInstDict[tPid][0] == 'cpy' \
                        and isinstance(unoptInstDict[tPid][2], int):
                    unoptInstDict[tPid] = ('nop',)
            currInstDict = optimizedInst(unoptInstDict)
        pid += pidOffset
    return register

print(executeInst({'a': 7, 'b': 0, 'c': 0, 'd': 0})['a'])

# print(executeInst({'a': 12, 'b': 0, 'c': 0, 'd': 0})['a'])

