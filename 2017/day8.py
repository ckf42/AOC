import AOCInit
import util
import operator as op

if __name__ != '__main__':
    exit()

inp = util.getInput(d=8, y=2017)

instList = tuple(l.split() for l in inp.splitlines())

# part 1
opDict = {
    '==': op.eq,
    '!=': op.ne,
    '>': op.gt,
    '<': op.lt,
    '>=': op.ge,
    '<=': op.le,
}
reg = dict()
maxV = 0

def getReg(n):
    if n[-1].isdigit():
        return int(n)
    if n not in reg:
        reg[n] = 0
    return reg[n]

for inst in instList:
    reg[inst[0]] = (getReg(inst[0])
                    + (1 if inst[1] == 'inc' else -1)
                    * int(inst[2])
                    * opDict[inst[5]](getReg(inst[4]), getReg(inst[6])))
    maxV = max(maxV, reg[inst[0]])
print(max(reg.values()))

# part 2
print(maxV)

