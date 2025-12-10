import AOCInit
import util
import sympy as sp
from sympy.solvers.diophantine import diophantine

if __name__ != '__main__':
    exit()

inp = """\
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
"""

# inp = util.getInput(d=10, y=2025)

machineSpec = []
for line in inp.splitlines():
    parts = line.split()
    target = tuple(c == '#' for c in parts[0][1:-1])
    jolt = util.getInts(parts[-1])
    btns = tuple(util.getInts(p) for p in parts[1:-1])
    machineSpec.append((target, btns, jolt))

# part 1

def applyBtn(state, btn):
    state = list(state)
    for i in btn:
        state[i] = not state[i]
    return tuple(state)

count = 0
for target, btns, _ in machineSpec:
    l = len(target)
    states = {(False,) * l: 0}
    for btn in btns:
        oldStates = states.copy()
        for state, presses in oldStates.items():
            newState = applyBtn(state, btn)
            states[newState] = min(states.get(newState, len(btns) + 1), presses + 1)
    count += states[target]
print(count)


# part 2

def applyBtnJolt(state, jolt):
    state = list(state)
    for i in jolt:
        state[i] += 1
    return tuple(state)

count = 0
for _, btns, target in machineSpec:
    l = len(target)
    btnVars = sp.symbols(f'a0:{len(btns)}', integer=True, nonnegative=True)
    equs = [v >= 0 for v in btnVars]
    for i, targetVal in enumerate(target):
        equPart = 0
        for bVar, btn in zip(btnVars, btns):
            if i in btn:
                equPart += bVar
        equs.append(sp.Eq(equPart, targetVal))
    print(btns, target)
    print(equs)
    print(sp.solve(equs, btnVars))
    # count += states[target]
print(count)




