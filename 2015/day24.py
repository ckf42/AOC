import AOCInit
import util
from ortools.sat.python import cp_model

if __name__ != '__main__':
    exit()

# TODO: optimize

itemList = util.getInts(util.getInput(d=24, y=2015))
itemCount = len(itemList)

def minqm(gpCount):
    partWeight = sum(itemList) // gpCount

    model = cp_model.CpModel()
    assignVarList = tuple(tuple(model.NewBoolVar(f'item{i}inGp{gp}')
                                for i in range(itemCount))
                        for gp in range(gpCount))
    for item in range(itemCount):
        model.AddExactlyOne(assignVarList[gp][item] for gp in range(gpCount))
    for gp in range(gpCount):
        model.Add(sum(assignVarList[gp][idx] * itemList[idx]
                    for idx in range(itemCount)) == partWeight)
    model.Minimize(sum(assignVarList[0]))
    print(model.ModelStats())
    print(model.Validate())

    solver = cp_model.CpSolver()
    solStatus = solver.Solve(model)
    print(solver.StatusName())
    if solStatus not in (cp_model.FEASIBLE, cp_model.OPTIMAL):
        print('failed finding solution')
    gp0Count = int(solver.ObjectiveValue())
    print('min gp0', gp0Count)

    model.ClearObjective()
    model.Add(sum(assignVarList[0]) == gp0Count)

    maxProd = util.prod(sorted(itemList, reverse=True)[:6])
    interProdVarList = [model.NewIntVar(1, maxProd, 'prod0')]
    model.Add(interProdVarList[0] == 1 + (itemList[0] - 1) * assignVarList[0][0])
    for idx in range(1, itemCount):
        interProdVarList.append(model.NewIntVar(1, maxProd, f'prod{idx}'))
        model.AddMultiplicationEquality(interProdVarList[idx],
                                        interProdVarList[idx - 1],
                                        1 + (itemList[idx] - 1) * assignVarList[0][idx])
    model.Minimize(interProdVarList[-1])
    solver = cp_model.CpSolver()
    solStatus = solver.Solve(model)
    print(solver.StatusName())
    if solStatus not in (cp_model.FEASIBLE, cp_model.OPTIMAL):
        print('failed finding solution')
    return int(solver.ObjectiveValue())


# part 1
print(minqm(3))

# part 2
print(minqm(4))


