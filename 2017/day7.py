import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=7, y=2017)

progList = dict()
for l in inp.splitlines():
    ls = l.split()
    progList[ls[0]] = (int(ls[1][1:-1]),
                       tuple(n.strip(',') for n in ls[3:])
                       if len(ls) > 2
                       else tuple())

# part 1
parentDict = dict()
for p, v in progList.items():
    for n in v[1]:
        parentDict[n] = p
root = (set(progList.keys()).difference(set(parentDict.keys()))).pop()
print(root)

# part 2
supportWeight = dict()
def getSupport(n):
    if n not in supportWeight:
        supportWeight[n] = progList[n][0] + sum(getSupport(nn) for nn in progList[n][1])
    return supportWeight[n]

ptr = root
while len((cList := progList[ptr][1])) != 0:
    pptr = util.argmax(cList, getSupport)
    if getSupport(pptr) == min(map(getSupport, cList)):
        break
    ptr = pptr
targetWeight = min(map(getSupport, progList[parentDict[ptr]][1]))
print(progList[ptr][0] + targetWeight - getSupport(ptr))

