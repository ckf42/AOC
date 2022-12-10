import AOCInit
import util
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2

if __name__ != '__main__':
    exit()

inp = util.getInput(d=13, y=2015).splitlines()
edgeDict = {(ls[0], ls[-1]): (-1 if ls[2] == 'lose' else 1) * int(ls[3])
            for l in inp
            if (ls := l.strip('.').split(' '))}
nameList = tuple(set(n for k in edgeDict for n in k))
nameCount = len(nameList)
for i in range(nameCount - 1):
    for j in range(i + 1, nameCount):
        v = edgeDict[(nameList[i], nameList[j])] + edgeDict[(nameList[j], nameList[i])]
        edgeDict[(nameList[i], nameList[j])] = v
        edgeDict[(nameList[j], nameList[i])] = v
maxDist = max(edgeDict.values())

def dist(*p):
    e = tuple(map(lambda x: nameList[x], p))
    return maxDist - edgeDict[e]

def getOptimal(costFunc, nodeCount):
    ctxMgr = pywrapcp.RoutingIndexManager(nodeCount, 1, 0)
    routing = pywrapcp.RoutingModel(ctxMgr)
    cb_idx = routing.RegisterTransitCallback(lambda x, y: costFunc(ctxMgr.IndexToNode(x),
                                                                   ctxMgr.IndexToNode(y)))
    routing.SetArcCostEvaluatorOfVehicle(cb_idx, 0)
    search_para = pywrapcp.DefaultRoutingSearchParameters()
    search_para.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    sol = routing.SolveWithParameters(search_para)
    return sol.ObjectiveValue()

# part 1
print(maxDist * nameCount - getOptimal(dist, nameCount))


# part 2
nameList = nameList + ('', )

def distPart2(*p):
    e = tuple(map(lambda x: nameList[x], p))
    if '' in e:
        return 0
    else:
        return maxDist - edgeDict[e]

print(maxDist * (nameCount - 1) - getOptimal(distPart2, 1 + nameCount))

