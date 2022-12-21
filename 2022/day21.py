import AOCInit
import util
import operator as op
import sympy as sp

if __name__ != '__main__':
    exit()

inp = util.getInput(d=21, y=2022)

instDict = {ls[0]: (sp.Rational(ls[1]) if ls[1].isdigit() else ls[1])
            for l in inp.splitlines()
            if (ls := l.split(': '))}

# part 1
reg = dict()
funcList = {
    '+': op.add,
    '-': op.sub,
    '*': op.mul,
    '/': op.truediv,
}

def getRes(n):
    if n not in reg:
        inst = instDict[n]
        if not isinstance(inst, str):
            reg[n] = inst
        else:
            inst = inst.split(' ')
            reg[n] = funcList[inst[1]](getRes(inst[0]), getRes(inst[2]))
    return reg[n]

print(getRes('root'))

# part 2
reg = dict()
x = sp.Symbol('x')
instDict['humn'] = x
rootInst = instDict['root'].split(' ')
print(sp.solvers.solve(getRes(rootInst[0]) - getRes(rootInst[2]), x))

