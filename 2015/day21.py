import AOCInit
import util
from ortools.sat.python import cp_model

if __name__ != '__main__':
    exit()

weapons = """Dagger        8     4       0
Shortsword   10     5       0
Warhammer    25     6       0
Longsword    40     7       0
Greataxe     74     8       0"""
armors = """Leather      13     0       1
Chainmail    31     0       2
Splintmail   53     0       3
Bandedmail   75     0       4
Platemail   102     0       5"""
rings = """Damage +1    25     1       0
Damage +2    50     2       0
Damage +3   100     3       0
Defense +1   20     0       1
Defense +2   40     0       2
Defense +3   80     0       3"""
weaponList = tuple(util.getInts(l) for l in weapons.splitlines())
armorList = tuple(util.getInts(l) for l in armors.splitlines())
ringList = tuple(util.getInts(l)[1:] for l in rings.splitlines())
wc = len(weaponList)
ac = len(armorList)
rc = len(ringList)
baseHp = 100
bossStat = util.getInts(util.getInput(d=21, y=2015))
maxDamageDeal = sum(item[1] for eqClass in (weaponList, armorList, ringList) for item in eqClass)
maxSpent = sum(item[0] for eqClass in (weaponList, armorList, ringList) for item in eqClass)

model = cp_model.CpModel()
weaponVarList = tuple(model.NewBoolVar(f'weapon{idx}') for idx in range(wc))
armorVarList = tuple(model.NewBoolVar(f'armor{idx}') for idx in range(ac))
ringVarList = tuple(model.NewBoolVar(f'ring{idx}') for idx in range(rc))
model.AddExactlyOne(*weaponVarList)
model.AddAtMostOne(*armorVarList)
model.Add(sum(ringVarList) <= 2)
damageVar = sum(c[idx][1] * v[idx]
                for c, v in zip((weaponList, ringList[:3]),
                                (weaponVarList, ringVarList[:3]))
                for idx in range(len(c)))
defenceVar = sum(c[idx][2] * v[idx]
                 for c, v in zip((armorList, ringList[3:]),
                                 (armorVarList, ringVarList[3:]))
                 for idx in range(len(c)))
costVar = sum(c[idx][0] * v[idx]
              for c, v in zip((weaponList, armorList, ringList),
                              (weaponVarList, armorVarList, ringVarList))
              for idx in range(len(c)))
damageDealVar = model.NewIntVar(1, maxDamageDeal, 'dam')
model.AddMaxEquality(damageDealVar, (damageVar - bossStat[2], 1))
damageTakeVar = model.NewIntVar(1, bossStat[1], 'def')
model.AddMaxEquality(damageTakeVar, (bossStat[1] - defenceVar, 1))
surviveTurn = model.NewIntVar(0, baseHp, 'survive')
model.AddDivisionEquality(surviveTurn, baseHp + damageTakeVar - 1, damageTakeVar)
killTure = model.NewIntVar(0, bossStat[0], 'kill')
model.AddDivisionEquality(killTure, bossStat[0] + damageDealVar - 1, damageDealVar)
needToWin = model.NewBoolVar('toWin')
model.Add(surviveTurn >= killTure).OnlyEnforceIf(needToWin)
model.Add(surviveTurn < killTure).OnlyEnforceIf(needToWin.Not())

# part 1
model.AddAssumption(needToWin)
model.Minimize(costVar)
print(model.ModelStats())
print(model.Validate())
solver = cp_model.CpSolver()
solStatus = solver.Solve(model)
print(solver.StatusName())
if solStatus in (cp_model.FEASIBLE, cp_model.OPTIMAL):
    print('cost', solver.Value(costVar))

# part 2
model.ClearAssumptions()
model.ClearObjective()
model.AddAssumption(needToWin.Not())
model.Maximize(costVar)
print(model.ModelStats())
print(model.Validate())
solver = cp_model.CpSolver()
solStatus = solver.Solve(model)
print(solver.StatusName())
if solStatus in (cp_model.FEASIBLE, cp_model.OPTIMAL):
    print('cost', solver.Value(costVar))

