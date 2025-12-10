import AOCInit
import util
import z3

if __name__ != '__main__':
    exit()


inp = util.getInput(d=10, y=2025)

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
    states = {(False,) * len(target): 0}
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
    btnVars = [z3.Int(f'x{i}') for i in range(len(btns))]
    equs = [v >= 0 for v in btnVars]
    for i, targetVal in enumerate(target):
        equPart = 0
        for bVar, btn in zip(btnVars, btns):
            if i in btn:
                equPart += bVar
        equs.append(equPart == targetVal)
    opt = z3.Optimize()
    opt.add(equs)
    cost = sum(btnVars)
    opt.minimize(cost)
    opt.check()
    count += opt.model().eval(cost).as_long()
print(count)




