import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=7, y=2018)
workerCount = 6
timeCost = lambda c: ord(c) + 1 - ord('A') + 60

# part 1
nodeList: set[str] = set()
# https://en.wikipedia.org/wiki/Topological_sorting#Kahn's_algorithm
# node: fromNode, toNode
edgeList: dict[str, tuple[set[str], set[str]]] = dict()
for line in inp.splitlines():
    ls = line.split()
    if ls[-3] not in edgeList:
        edgeList[ls[-3]] = (set(), set())
    if ls[1] not in edgeList:
        edgeList[ls[1]] = (set(), set())
    edgeList[ls[-3]][0].add(ls[1])
    edgeList[ls[1]][1].add(ls[-3])
    nodeList.update((ls[-3], ls[1]))
nodeCount = len(nodeList)
orderList = list()
rootList = util.MinHeap(filter(lambda n: len(edgeList[n][0]) == 0, nodeList))
while not rootList.isEmpty():
    c = rootList.pop()
    orderList.append(c)
    for n in edgeList[c][1]:
        edgeList[n][0].remove(c)
        if len(edgeList[n][0]) == 0:
            rootList.push(n)
print(''.join(orderList))

# part 2
edgeList.clear()
for line in inp.splitlines():
    ls = line.split()
    if ls[-3] not in edgeList:
        edgeList[ls[-3]] = (set(), set())
    if ls[1] not in edgeList:
        edgeList[ls[1]] = (set(), set())
    edgeList[ls[-3]][0].add(ls[1])
    edgeList[ls[1]][1].add(ls[-3])
    nodeList.update((ls[-3], ls[1]))
# (available time, char)
availableTimeHeap = util.MinHeap(tuple((0, None) for _ in range(workerCount)),
                                 lambda pr: pr[0])
untouchedWorkCount = nodeCount
rootList = util.MinHeap(tuple(filter(lambda c: len(edgeList[c][0]) == 0, nodeList)))
currTime = 0
while untouchedWorkCount > 0:
    while rootList.isEmpty() or len(availableTimeHeap) == workerCount:
        # wait till some worker finish
        worker = availableTimeHeap.pop()
        currTime = worker[0]
        if (c := worker[1]) is not None:
            for n in edgeList[c][1]:
                edgeList[n][0].remove(c)
                if len(edgeList[n][0]) == 0:
                    rootList.push(n)
    c = rootList.pop()
    untouchedWorkCount -= 1
    availableTimeHeap.push((currTime + timeCost(c), c))
    # make free worker instantly available
    for _ in range(len(availableTimeHeap), workerCount):
        availableTimeHeap.push((currTime, None))
while not availableTimeHeap.isEmpty():
    currTime = availableTimeHeap.pop()[0]
print(currTime)

