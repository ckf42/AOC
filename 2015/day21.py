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
Defense +3   80     0       3
"""
weaponList = tuple(util.getInts(l) for l in weapons.splitlines())
armorList = tuple(util.getInts(l) for l in armors.splitlines())
ringList = tuple(util.getInts(l)[1:] for l in rings.splitlines())
wc = len(weaponList)
ac = len(armorList)
rc = len(ringList)
baseHp = 100
bossStat = util.getInts(util.getInput(d=21, y=2015))
# maxDamageDeal = sum(item[1] for eqClass in (weaponList, armors, ringList) for item in eqClass)

# part 1
model = cp_model.CpModel()
weaponVarList = list()
armorVarList = list()
ringVarList = list()
for idx in range(wc):
    weaponVarList.append(model.NewBoolVar(f'weapon{idx}'))
for idx in range(ac):
    armorVarList.append(model.NewBoolVar(f'armor{idx}'))
for idx in range(rc):
    ringVarList.append(model.NewBoolVar(f'ring{idx}'))
model.AddExactlyOne(*weaponVarList)
model.AddAtMostOne(*armorVarList)
model.Add(sum(ringVarList) <= 2)
damageVar = sum(c[idx][1] * v[idx]
                for c, v in zip((weaponList, ringList),
                                (weaponVarList, ringVarList))
                for idx in range(len(c)))
defenceVar = sum(c[idx][2] * v[idx]
                 for c, v in zip((armorList, ringList),
                                 (armorVarList, ringVarList))
                 for idx in range(len(c)))
costVar = sum(c[idx][0] * v[idx]
              for c, v in zip((weaponList, armorList, ringList),
                              (weaponVarList, armorVarList, ringVarList))
              for idx in range(len(c)))
# damageDealVar = model.NewIntVar(1, maxDamageDeal, 'dam')
# damageTakeVar = model.NewIntVar(1, bossStat[1], 'dam')
# model.AddMaxEquality(damageDealVar)
model.Add(baseHp * max(damageVar - bossStat[2], 1) >= bossStat[0] * max(bossStat[1] - defenceVar, 1))
model.Minimize(costVar)

# part 2

