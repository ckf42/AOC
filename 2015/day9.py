import AOCInit
import util
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2

if __name__ != '__main__':
    exit()

inp = util.getInput(d=9, y=2015).splitlines()
edgeDict = {(ls[0], ls[2]): int(ls[4]) for l in inp if (ls := l.split())}
maxDist = max(edgeDict.values())
edgeDict.update({p[::-1]: v for p, v in edgeDict.items()})
loc = ('', ) + tuple(set(loc for e in edgeDict for loc in e[:-1]))


def getDist(*p):
    e = tuple(map(lambda x: loc[x], p))
    return 0 if '' in e else edgeDict[e]

def getRevDist(*p):
    e = tuple(map(lambda x: loc[x], p))
    return 0 if '' in e else maxDist - edgeDict[e]

def getOptimal(costFunc):
    ctxMgr = pywrapcp.RoutingIndexManager(len(loc), 1, 0)
    routing = pywrapcp.RoutingModel(ctxMgr)
    cb_idx = routing.RegisterTransitCallback(lambda x, y: costFunc(ctxMgr.IndexToNode(x),
                                                                   ctxMgr.IndexToNode(y)))
    routing.SetArcCostEvaluatorOfVehicle(cb_idx, 0)
    search_para = pywrapcp.DefaultRoutingSearchParameters()
    search_para.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    sol = routing.SolveWithParameters(search_para)
    return sol.ObjectiveValue() if sol else -float('Inf')

# part 1
print(getOptimal(getDist))

# part 2
print((len(loc) - 2) * maxDist - getOptimal(getRevDist))

