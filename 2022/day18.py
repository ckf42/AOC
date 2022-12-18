import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=18, y=2022)
blocks = set(util.getInts(l) for l in inp.splitlines())

dirVect = [0, 0, 0]
directions = list()
for i in range(3):
    for m in (-1, 1):
        dirVect[i] = m
        directions.append(tuple(dirVect))
    dirVect[i] = 0

# part 1
surfaceCount = 0
for b in blocks:
    for d in directions:
        if not tuple(b[i] + d[i] for i in range(3)) in blocks:
            surfaceCount += 1
print(surfaceCount)

# part 2
maxRange = tuple(max(b[i] for b in blocks) for i in range(3))
minRange = tuple(min(b[i] for b in blocks) for i in range(3))
visited = set()
outerSurfaceCount = 0

# circumvent recursion overflow
# TODO: should not have deep recursion depth. check why
stack = list()
def visit(pt):
    global outerSurfaceCount
    if pt in visited:
        return
    visited.add(pt)
    nei = tuple(tuple(pt[i] + d[i] for i in range(3))
                for d in directions
                if all(minRange[j] - 1 <= pt[j] + d[j] <= maxRange[j] + 1
                       for j in range(3)))
    for n in nei:
        if n in blocks:
            outerSurfaceCount += 1
        elif n not in visited:
            stack.append(n)

stack.append(tuple(r - 1 for r in minRange))
while len(stack) != 0:
    visit(stack.pop())
print(outerSurfaceCount)

