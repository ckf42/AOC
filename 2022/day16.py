import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=16, y=2022).splitlines()
# inp = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
# Valve BB has flow rate=13; tunnels lead to valves CC, AA
# Valve CC has flow rate=2; tunnels lead to valves DD, BB
# Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
# Valve EE has flow rate=3; tunnels lead to valves FF, DD
# Valve FF has flow rate=0; tunnels lead to valves EE, GG
# Valve GG has flow rate=0; tunnels lead to valves FF, HH
# Valve HH has flow rate=22; tunnel leads to valve GG
# Valve II has flow rate=0; tunnels lead to valves AA, JJ
# Valve JJ has flow rate=21; tunnel leads to valve II""".splitlines()
valveList = tuple([ls[1], util.getInts(ls[4])[0], list(v.strip(',') for v in ls[9:])]
                  for l in inp
                  if (ls := l.split()))
valveCount = len(valveList)
nameDict = {v[0]: i for i, v in enumerate(valveList)}
for i in range(valveCount):
    valveList[i][2] = tuple(map(lambda n: nameDict[n], valveList[i][2]))
mValveList = tuple(sorted(filter(lambda i: valveList[i][1] != 0,
                                 range(valveCount)),
                          key=lambda i: valveList[i][1],
                          reverse=True))
mValveCount = len(mValveList)
mValveDict = {vidx: i for i, vidx in enumerate(mValveList)}
print(mValveDict)

# part 1
# currently wasted, time remain, loc, meaningfulValves on/off
# timeLimit = 30
# initialNode = (0, timeLimit, nameDict['AA']) + (False,) * mValveCount

# def aStarH(st):
    # wastedRate = sorted((valveList[i][1] for i in mValveList if not st[3 + mValveDict[i]]),
                        # reverse=True)
    # return sum(wastedRate[t] * (t + 1) for t in range(min(st[1], len(wastedRate))))

# h = util.MinHeap(initItemList=(initialNode,),
                 # key=lambda st: st[0] + aStarH(st))
# visited = set()
# optimalState = None
# while not h.isEmpty():
    # state = h.pop()
    # if state[1] == 0 or all(state[3:]):
        # print(state)
        # optimalState = state
        # break
    # if state in visited:
        # continue
    # visited.add(state)
    # mState = list(state)
    # mState[1] -= 1
    # stepCost = sum(valveList[i][1] for i in mValveList if not state[3 + mValveDict[i]])
    # mState[0] += stepCost
    # if state[2] in mValveDict and not state[3 + mValveDict[state[2]]]:
        # mState[3 + mValveDict[state[2]]] = True
        # newNode = tuple(mState)
        # if newNode not in visited:
            # h.push(newNode)
        # mState[3 + mValveDict[state[2]]] = False
    # for target in valveList[state[2]][2]:
        # mState[2] = target
        # newNode = tuple(mState)
        # if newNode not in visited:
            # h.push(newNode)
# print(sum(valveList[i][1] for i in mValveList) * timeLimit - optimalState[0])

# part 2
# should work but killed after ~10 min and 3GM RAM with 8.6M nodes in heap
# TODO: optimize this (maybe next week?)
# currently wasted, time remain, loc, ele loc, meaningfulValves on/off
timeLimit = 26
initialNode = (0, timeLimit, nameDict['AA'], nameDict['AA']) + (False,) * mValveCount

def aStarH2(st):
    wastedRateGps = util.splitIntoGp(
            tuple(valveList[i][1]
                  for i in mValveList
                  if not st[4 + mValveDict[i]]),
            gpSize=2, allowRemain=True)
    return sum(sum(gp) * (2 * t + 1) for t, gp in enumerate(wastedRateGps))

h = util.MinHeap(initItemList=(initialNode,),
                 key=lambda st: st[0] + aStarH2(st))
visited = set()

def isVisited(state):
    return state in visited \
            or (state[2] != state[3] \
                    and (state[0:2] + state[3:1:-1] + state[4:]) in visited)

optimalState = None
while not h.isEmpty():
    print(len(h))
    state = h.pop()
    if state[1] == 0 or all(state[4:]):
        print(state)
        optimalState = state
        break
    if isVisited(state):
        continue
    # print(state)
    visited.add(state)
    mState = list(state)
    mState[1] -= 1
    stepCost = sum(valveList[i][1] for i in mValveList if not state[4 + mValveDict[i]])
    mState[0] += stepCost
    selfActions = valveList[state[2]][2] \
            + ((None,)
               if state[2] in mValveList and not state[4 + mValveDict[state[2]]]
               else ())
    eleActions = valveList[state[3]][2] \
            + ((None,)
               if state[3] in mValveList and not state[4 + mValveDict[state[3]]]
               else ())
    for selfAct in selfActions:
        if selfAct is None:
            mState[4 + mValveDict[state[2]]] = True
        else:
            mState[2] = selfAct
        for eleAct in eleActions:
            if eleAct is None:
                mState[4 + mValveDict[state[3]]] = True
            else:
                mState[3] = eleAct
            newNode = tuple(mState)
            if not isVisited(newNode):
                h.push(newNode)
            if eleAct is None:
                mState[4 + mValveDict[state[3]]] = False
            else:
                mState[3] = state[3]
        if selfAct is None:
            mState[4 + mValveDict[state[2]]] = False
        else:
            mState[2] = state[2]
print(sum(valveList[i][1] for i in mValveList) * timeLimit - optimalState[0])

