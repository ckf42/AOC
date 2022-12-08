import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=7, y=2015).splitlines()

opDict = {
    'AND': (lambda x, y: x & y),
    'OR': (lambda x, y: x | y),
    'LSHIFT': (lambda x, y: (x << y) % 65536),
    'RSHIFT': (lambda x, y: x >> y),
    'ID': (lambda x: x),
    'NOT': (lambda x: 65536 + ~x),
}
valDict = dict()
depDict = dict()

# part 1
for inst in inp:
    (cmd, target) = inst.split(' -> ', maxsplit=1)
    cmdList = cmd.split(' ')
    if len(cmdList) == 1:
        # assignment
        depDict[target] = ('ID', (cmdList[0], ))
    elif len(cmdList) == 2:
        # not
        depDict[target] = ('NOT', (cmdList[1], ))
    else:
        # other
        depDict[target] = (cmdList[1], (cmdList[0], cmdList[2]))

def getVal(val):
    if val[0].isdigit():
        return int(val)
    else:
        if val not in valDict:
            dep = depDict[val]
            valDict[val] = opDict[dep[0]](*map(getVal, dep[1]))
        return valDict[val]

aVal = getVal('a')
print(aVal)

# part 2
valDict = {'b': aVal}
print(getVal('a'))

