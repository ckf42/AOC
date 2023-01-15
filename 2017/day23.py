import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=23, y=2017)

instList = {
    i: tuple((int(term) if term[-1].isdigit() else term) for term in line.split())
    for i, line in enumerate(inp.splitlines())
}
l = len(instList)

# part 1
mulCount = 0
register = {chr(ord('a') + i): 0 for i in range(8)}
pid = 0
while pid < l:
    inst = instList[pid]
    pidOffset = 1
    if inst[0] == 'set':
        register[inst[1]] = register.get(inst[2], inst[2])
    elif inst[0] == 'sub':
        register[inst[1]] -= register.get(inst[2], inst[2])
    elif inst[0] == 'mul':
        mulCount += 1
        register[inst[1]] *= register.get(inst[2], inst[2])
    elif inst[0] == 'jnz':
        if register.get(inst[1], inst[1]) != 0:
            pidOffset = register.get(inst[2], inst[2])
    pid += pidOffset
print(mulCount)

# TODO: need optimize
# part 2
register = {chr(ord('a') + i): 0 for i in range(8)}
register['a'] = 1
pid = 0
while pid < l:
    inst = instList[pid]
    pidOffset = 1
    if inst[0] == 'set':
        register[inst[1]] = register.get(inst[2], inst[2])
    elif inst[0] == 'sub':
        register[inst[1]] -= register.get(inst[2], inst[2])
    elif inst[0] == 'mul':
        register[inst[1]] *= register.get(inst[2], inst[2])
    elif inst[0] == 'jnz':
        if register.get(inst[1], inst[1]) != 0:
            pidOffset = register.get(inst[2], inst[2])
    pid += pidOffset
print(register['h'])

