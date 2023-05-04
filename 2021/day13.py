import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=13, y=2021)

(ptLines, instLines) = inp.split('\n\n')
pts = set(tuple(util.getInts(line))
          for line in ptLines.splitlines())
instructions = tuple(
    (parts[0], int(parts[1]))
    for line in instLines.splitlines()
    if (parts := line.rsplit(' ', maxsplit=1)[-1].split('='))
)

# part 1
for axis, loc in instructions[:1]:
    ptsToMove = frozenset(filter(lambda pt: pt[1 if axis == 'y' else 0] > loc, pts))
    for pt in ptsToMove:
        pts.remove(pt)
        if axis == 'y':
            pts.add((pt[0], 2 * loc - pt[1]))
        else:
            pts.add((2 * loc - pt[0], pt[1]))
print(len(pts))

# part 2
for axis, loc in instructions[1:]:
    ptsToMove = frozenset(filter(lambda pt: pt[1 if axis == 'y' else 0] > loc, pts))
    for pt in ptsToMove:
        pts.remove(pt)
        if axis == 'y':
            pts.add((pt[0], 2 * loc - pt[1]))
        else:
            pts.add((2 * loc - pt[0], pt[1]))
bds = util.rangeBoundOnCoors(pts)
for j in util.inclusiveRange(*bds[1]):
    for i in util.inclusiveRange(*bds[0]):
        print(util.consoleChar((i, j) in pts), end='')
    print('')

