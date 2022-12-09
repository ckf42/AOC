import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=23, y=2015).splitlines()
# inp = 'inc a\njio a, +2\ntpl a\ninc a'.splitlines()
l = len(inp)
instList = list(list(c.strip(',') for c in l.split(' ')) for l in inp)
for lineNum, cmd in enumerate(instList):
    if cmd[0] in ('jie', 'jio'):
        cmd[2] = lineNum + int(cmd[2])
    elif cmd[0] == 'jmp':
        cmd[1] = lineNum + int(cmd[1])

# part 1
pip = 0
reg = {'a': 0, 'b': 0}
while pip != l:
    cmd = instList[pip]
    if cmd[0][0] == 'j':
        if cmd[0] == 'jmp':
            pip = cmd[1]
        elif cmd[0] == 'jie':
            pip = (pip + 1 if reg[cmd[1]] & 1 else cmd[2])
        else:
            pip = (cmd[2] if reg[cmd[1]] == 1 else pip + 1)
    else:
        if cmd[0] == 'hlf':
            reg[cmd[1]] //= 2
        elif cmd[0] == 'tpl':
            reg[cmd[1]] *= 3
        elif cmd[0] == 'inc':
            reg[cmd[1]] += 1
        pip += 1
print(reg['b'])

# part 2
pip = 0
reg = {'a': 1, 'b': 0}
while pip != l:
    cmd = instList[pip]
    if cmd[0][0] == 'j':
        if cmd[0] == 'jmp':
            pip = cmd[1]
        elif cmd[0] == 'jie':
            pip = (pip + 1 if reg[cmd[1]] & 1 else cmd[2])
        else:
            pip = (cmd[2] if reg[cmd[1]] == 1 else pip + 1)
    else:
        if cmd[0] == 'hlf':
            reg[cmd[1]] //= 2
        elif cmd[0] == 'tpl':
            reg[cmd[1]] *= 3
        elif cmd[0] == 'inc':
            reg[cmd[1]] += 1
        pip += 1
print(reg['b'])

