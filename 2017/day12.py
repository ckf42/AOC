import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=12, y=2017)

edgeDict = dict()
for l in inp.splitlines():
    vals = util.getInts(l)
    edgeDict[vals[0]] = vals[1:]

# part 1
visitedState = set()
stack = list()
stack.append(0)
while len(stack) != 0:
    p = stack.pop()
    if p in visitedState:
        continue
    visitedState.add(p)
    stack.extend(edgeDict[p])
print(len(visitedState))

# part 2
gpCount = 1
for k in edgeDict:
    if k not in visitedState:
        gpCount += 1
        stack = list()
        stack.append(k)
        while len(stack) != 0:
            p = stack.pop()
            if p in visitedState:
                continue
            visitedState.add(p)
            stack.extend(edgeDict[p])
print(gpCount)

