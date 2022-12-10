import AOCInit
import util
from ortools.sat.python import cp_model

if __name__ != '__main__':
    exit()

inp = util.getInput(d=15, y=2015).splitlines()
ingre = tuple(util.getInts(l) for l in inp)
ingreCount = len(ingre)
propCount = 4

model = cp_model.CpModel()
varList = list(model.NewIntVar(0, 100, f'ingre{i}') for i in range(ingreCount))
model.Add(sum(varList) == 100)
propValList = list()
propRange = list()
for prop in range(propCount):
    propRange.append(max(abs(ing[prop]) for ing in ingre) * 100)
    propValList.append(model.NewIntVar(-propRange[-1], propRange[-1], f'prop{prop}'))
    model.Add(propValList[-1] == sum(ingre[idx][prop] * varList[idx]
                                     for idx in range(ingreCount)))
    model.Add(propValList[-1] > 0)
productList = [propValList[0], ]
for prop in range(1, propCount):
    bd = util.prod(propRange[:(prop + 1)])
    productList.append(model.NewIntVar(-bd, bd, f'mul[0:{prop}]'))
    model.AddMultiplicationEquality(productList[prop],
                                    productList[prop - 1], propValList[prop])
model.Maximize(productList[-1])
print(model.ModelStats())

# part 1
solver = cp_model.CpSolver()
solStatus = solver.Solve(model)
print(solver.StatusName())
if solStatus in (cp_model.FEASIBLE, cp_model.OPTIMAL):
    for i, v in enumerate(varList):
        print(i, solver.Value(v))
    print('val', solver.Value(productList[-1]))

# part 2
model.Add(sum(varList[idx] * ingre[idx][-1] for idx in range(ingreCount)) == 500)
solver = cp_model.CpSolver()
solStatus = solver.Solve(model)
print(solver.StatusName())
if solStatus in (cp_model.FEASIBLE, cp_model.OPTIMAL):
    for i, v in enumerate(varList):
        print(i, solver.Value(v))
    print('val', solver.Value(productList[-1]))

