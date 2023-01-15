import AOCInit
import util

if __name__ != '__main__':
    exit()

# TODO: find ways to optimize this

inp = util.getInput(d=12, y=2016).splitlines()
l = len(inp)
instDict = {i: tuple((int(term) if term[-1].isdigit() else term)
                     for term in l.split())
            for i, l in enumerate(inp)}

# optimize instructions
for i in range(1, l - 1):
    if instDict[i][0] == 'dec' \
            and instDict[i + 1] == ('jnz', instDict[i][1], -2) \
            and instDict[i - 1][0] in ('inc', 'dec') \
            and instDict[i - 1][1] != instDict[i][1]:
        instDict[i - 1] = (
                '+=' if instDict[i - 1][0] == 'inc' else '-=',
                instDict[i - 1][1],
                instDict[i][1]
        )
        instDict[i] = instDict[i + 1] = ('nop',)

def executeInst(register):
    pid = 0
    while pid < l:
        inst = instDict[pid]
        pidOffset = 1
        if inst[0] == 'cpy':
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
        elif inst[0] == 'nop':
            pass
        pid += pidOffset
    return register

# part 1
print(executeInst({'a': 0, 'b': 0, 'c': 0, 'd': 0})['a'])

# part 2
print(executeInst({'a': 0, 'b': 0, 'c': 1, 'd': 0})['a'])


