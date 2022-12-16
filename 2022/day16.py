import AOCInit
import util

if __name__ != '__main__':
    exit()

# inp = util.getInput(d=16, y=2022).splitlines()
inp = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II""".splitlines()
valveList = tuple([ls[1], util.getInts(ls[4])[0], list(v.strip(',') for v in ls[9:])]
                  for l in inp
                  if (ls := l.split()))
valveCount = len(valveList)
valveNameDict = {v[0]: i for i, v in enumerate(valveList)}
for i in range(valveCount):
    valveList[i][2] = tuple(map(lambda n: valveNameDict[n], valveList[i][2]))

# part 1
# ?
# released, remain time, current loc, on/off state

# def aStarDist(state):
    # vals = sorted((valveList[i][1] for i in range(valveCount) if not state[3 + i]), reverse=True)
    # return state[0] + sum(val * (state[1] - 1 - order) for order, val in enumerate(vals))

# initState = (0, 30, valveNameDict['AA'],) + (False,) * valveCount
# h = util.MaxHeap(initItemList=(initState,), key=aStarDist)
# optimalVal = 0
# visited = set()
# while not h.isEmpty():
    # print(len(h))
    # state = h.pop()
    # optimalVal = max(optimalVal, state[0])
    # if state[1] == 0:
        # print(state)
        # break
    # if state in visited:
        # continue
    # visited.add(state)
    # if not state[3 + state[2]] and valveList[state[2]][1] != 0:
        # # open valve of idx state[2]
        # newNode = (state[0] + valveList[state[2]][1] * (state[1] - 1), state[1] - 1) \
                # + state[2:3 + state[2]] + (True,) + state[4 + state[2]:]
        # if newNode not in visited:
            # h.push(newNode)
    # for loc in valveList[state[2]][2]:
        # newNode = (state[0], state[1] - 1, loc) + state[3:]
        # if newNode not in visited:
            # h.push(newNode)
# print(optimalVal)

# part 2
# released, remain time, current loc, ele loc, on/off state
# initState = (0, 26, valveNameDict['AA'], valveNameDict['AA']) + (False,) * valveCount
# h = util.MaxHeap(initItemList=(initState,), key=lambda st: st[0])
# visited = set()
# optimalVal = 0
# while not h.isEmpty():
    # state = h.pop()
    # optimalVal = max(optimalVal, state[0])
    # if state[1] == 0:
        # print(state)
            # continue
    # if state in visited:
        # continue
    # visited.add(state)
    # mState = list(state)
    # mState[1] -= 1
    # if any(not state[4 + state[i]] and valveList[state[i]][1] != 0 for i in (2, 3)):
        # mState[4 + state[2]] = mState[4 + state[3]] = True
        # mState[0] += mState[1] * sum(valveList[i][1]
                                     # for i in {state[2], state[3]}
                                     # if not state[4 + i])
        # newState = tuple(mState)
        # if newState not in visited:
            # h.push(newState)
        # mState[0] = state[0]
        # mState[4 + state[2]] = state[4 + state[2]]
        # mState[4 + state[3]] = state[4 + state[3]]
    # for newLoc in (state[2],) + valveList[state[2]][2]:
        # mState[2] = newLoc
        # for newEleLoc in (state[3],) + valveList[state[3]][2]:
            # if newLoc == state[2] and newEleLoc == state[3]:
                # continue
            # mState[3] = newEleLoc
            # newState = tuple(mState)
            # if newState not in visited:
                # h.push(newState)
# print(optimalVal)
