import AOCInit
import util
from functools import cache

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
@cache
def mask(n):
    return 1 << n

def applyBtn(state, btn):
    return state ^ sum(mask(i) for i in btn)

count = 0
for target, btns, _ in machineSpec:
    targetVal = applyBtn(0, [i for i, v in enumerate(target) if v])
    states = {0: 0}
    for btn in btns:
        for state, presses in states.copy().items():
            newState = applyBtn(state, btn)
            states[newState] = min(states.get(newState, len(btns) + 1), presses + 1)
    count += states[targetVal]
print(count)


# part 2
# using idea by [u/tenthmascot](https://redd.it/1pk87hl)
count = 0
for _, btns, target in machineSpec:
    states = {0: [tuple()]}
    for bidx, btn in enumerate(btns):
        for state, lst in states.copy().items():
            newState = applyBtn(state, btn)
            if newState not in states:
                states[newState] = list()
            for choice in lst:
                states[newState].append(choice + (bidx,))
    @cache
    def solve(values):
        if all(x == 0 for x in values):
            return 0
        res = float('inf')
        for btnChoice in states.get(sum(mask(i) for i, x in enumerate(values) if x % 2 != 0), list()):
            valLst = list(values)
            for bidx in btnChoice:
                for i in btns[bidx]:
                    valLst[i] -= 1
            if any(x < 0 for x in valLst):
                continue
            res = min(res, solve(tuple(x // 2 for x in valLst)) * 2 + len(btnChoice))
        return res
    count += solve(target)
print(count)



