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

# part 1
register = {'a': 0, 'b': 0, 'c': 0, 'd': 0}
pid = 0
while pid < l:
    inst = instDict[pid]
    if inst[0] == 'cpy':
        register[inst[2]] = register.get(inst[1], inst[1])
        pid += 1
    elif inst[0] == 'inc':
        register[inst[1]] += 1
        pid += 1
    elif inst[0] == 'dec':
        register[inst[1]] -= 1
        pid += 1
    else:
        pid += 1 if register.get(inst[1], inst[1]) == 0 else inst[2]
print(register['a'])

# part 2
register = {'a': 0, 'b': 0, 'c': 1, 'd': 0}
pid = 0
while pid < l:
    inst = instDict[pid]
    if inst[0] == 'cpy':
        register[inst[2]] = register.get(inst[1], inst[1])
        pid += 1
    elif inst[0] == 'inc':
        register[inst[1]] += 1
        pid += 1
    elif inst[0] == 'dec':
        register[inst[1]] -= 1
        pid += 1
    else:
        pid += 1 if register.get(inst[1], inst[1]) == 0 else inst[2]
print(register['a'])


