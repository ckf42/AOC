import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=18, y=2020)

def calc(expr: str) -> int:
    while (openIdx := expr.find('(')) != -1:
        closeIdx = util.matchClosingBracket(expr, openIdx, ')', escapeChar=None)
        assert closeIdx is not None
        expr = expr[:openIdx] + str(calc(expr[openIdx + 1:closeIdx])) + expr[closeIdx + 1:]
    numbers = util.getInts(expr)
    opers = tuple(c for c in expr if c in '+*')
    assert len(numbers) == len(opers) + 1
    res = numbers[0]
    for (val, op) in zip(numbers[1:], opers):
        res = (res + val) if op == '+' else (res * val)
    return res

# part 1
print(sum(calc(line) for line in inp.splitlines()))


# part 2
def advancedCalc(expr: str) -> int:
    while (openIdx := expr.find('(')) != -1:
        closeIdx = util.matchClosingBracket(expr, openIdx, ')', escapeChar=None)
        assert closeIdx is not None
        expr = expr[:openIdx] + str(advancedCalc(expr[openIdx + 1:closeIdx])) + expr[closeIdx + 1:]
    numbers = list(util.getInts(expr))
    opers = list(c for c in expr if c in '+*')
    assert len(numbers) == len(opers) + 1
    idx = len(opers) - 1
    while idx >= 0:
        if opers[idx] == '+':
            opers[idx:idx + 1] = []
            numbers[idx:idx + 2] = [sum(numbers[idx:idx + 2])]
        idx -= 1
    return util.prod(numbers)
print(sum(advancedCalc(line) for line in inp.splitlines()))

