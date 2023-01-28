import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = """\
x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504\
"""
# inp = util.getInput(d=17, y=2018)

maxY = -util.inf
clayBlocks = set()
for l in inp.splitlines():
    ls = util.getInts(l)
    assert len(ls) == 3
    if l[0] == 'x':
        for i in util.inclusiveRange(ls[1], ls[2]):
            clayBlocks.add(complex(ls[0], i))
        maxY = max(maxY, ls[1])
    else:
        for i in util.inclusiveRange(ls[1], ls[2]):
            clayBlocks.add(complex(i, ls[0]))
        maxY = max(maxY, ls[0])
waterBlocks = set()
pointsToExpand = [(complex(500, 0), 'd')]

# part 1
while len(pointsToExpand) != 0:
    (pt, mode) = pointsToExpand.pop()
    if pt in waterBlocks or pt in clayBlocks or int(pt.imag) > maxY:
        continue
    waterBlocks.add(pt)
    if mode == 'd':



# part 2


