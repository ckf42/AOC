import AOCInit
import util
import re
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2

if __name__ != '__main__':
    exit()

inp = """\
###########
#0.1.....2#
#.#######.#
#4.......3#
###########\
"""
inp = util.getInput(d=24, y=2016)

board = inp.splitlines()
boardDim = util.Point(len(board), len(board[0]))
digitLoc = {int(m.group()): util.Point.fromIterable(divmod(m.start(), boardDim[1] + 1))
            for m in re.finditer(r'\d', inp)}
digitCount = len(digitLoc)

directions = tuple(util.Point.fromIterable(d)
                   for d in util.integerLattice(2, 1))

def getNei(pt):
    resList = list()
    for d in directions:
        newPt = pt + d
        if 0 <= newPt < boardDim and board[newPt[0]][newPt[1]] != '#':
            resList.append(newPt)
    return resList

digitDist = dict()
for i in range(digitCount - 1):
    for j in range(i + 1, digitCount):
        digitDist[(i, j)] = util.dijkstra(digitLoc[i],
                                          lambda nst, ost, oc: oc + 1,
                                          getNei,
                                          lambda pt: pt == digitLoc[j],
                                          lambda pt: (pt - digitLoc[j]).norm(1))[1]
        digitDist[(j, i)] = digitDist[(i, j)]

for i in range(digitCount):
    digitDist[(i, digitCount)] = digitDist[(digitCount, i)] = 0

# part 1
ctxMgr = pywrapcp.RoutingIndexManager(digitCount + 1, 1, digitCount)
routing = pywrapcp.RoutingModel(ctxMgr)
# remove edge from digitCount to other
for i in range(1, digitCount):
    routing.NextVar(ctxMgr.NodeToIndex(digitCount)).RemoveValue(ctxMgr.NodeToIndex(i))
cb_idx = routing.RegisterTransitCallback(lambda x, y: digitDist[(ctxMgr.IndexToNode(x),
                                                                 ctxMgr.IndexToNode(y))])
routing.SetArcCostEvaluatorOfAllVehicles(cb_idx)
search_para = pywrapcp.DefaultRoutingSearchParameters()
search_para.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
sol = routing.SolveWithParameters(search_para)
print(sol.ObjectiveValue() if sol else -float('Inf'))

# part 2
ctxMgr = pywrapcp.RoutingIndexManager(digitCount, 1, 0)
routing = pywrapcp.RoutingModel(ctxMgr)
cb_idx = routing.RegisterTransitCallback(lambda x, y: digitDist[(ctxMgr.IndexToNode(x),
                                                                 ctxMgr.IndexToNode(y))])
routing.SetArcCostEvaluatorOfAllVehicles(cb_idx)
search_para = pywrapcp.DefaultRoutingSearchParameters()
search_para.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
sol = routing.SolveWithParameters(search_para)
print(sol.ObjectiveValue() if sol else -float('Inf'))

