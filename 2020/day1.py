import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=1, y=2020)

# part 1
expense = sorted(util.getInts(inp))

def sumsTo(goal, s):
    ptrs = [s, len(expense) - 1]
    while ptrs[0] < ptrs[1]:
        s = sum(expense[i] for i in ptrs)
        if s == goal:
            return (expense[ptrs[0]], expense[ptrs[1]])
        elif s < goal:
            ptrs[0] += 1
        else:
            ptrs[1] -= 1
    return None

twoProd = sumsTo(2020, 0)
assert twoProd is not None
print(twoProd[0] * twoProd[1])

# part 2
for i in range(len(expense) - 2):
    threeProd = sumsTo(2020 - expense[i], i + 1)
    if threeProd is not None:
        print(expense[i] * threeProd[0] * threeProd[1])
        break


