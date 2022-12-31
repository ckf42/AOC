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
register = {'a': 7, 'b': 0, 'c': 0, 'd': 0}
pid = 0
while pid < l:
    inst = instDict[pid]
    # print(inst, register)
    pidOffset = 1
    if inst[0] == 'cpy':
        if isinstance(inst[2], str):
            register[inst[2]] = register.get(inst[1], inst[1])
    elif inst[0] == 'inc':
        register[inst[1]] += 1
    elif inst[0] == 'dec':
        register[inst[1]] -= 1
    elif inst[0] == 'jnz':
        pidOffset = 1 \
                if register.get(inst[1], inst[1]) == 0 \
                else (inst[2]
                      if isinstance(inst[2], int)
                      else register[inst[2]])
    else:
        # tgl
        if 0 <= (targetPid := pid + (int(inst[1])
                                     if inst[1][-1].isdigit()
                                     else register[inst[1]])) < l:
            newInst = list(instDict[targetPid])
            if len(newInst) == 2:
                newInst[0] = ('dec' if newInst[0] == 'inc' else 'inc')
            else:
                newInst[0] = ('cpy' if newInst[0] == 'jnz' else 'jnz')
            instDict[targetPid] = tuple(newInst)
    pid += pidOffset
print(register['a'])




