import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=4, y=2024)

lines = inp.splitlines()
patt = 'XMAS'

# part 1
count = sum(
    len(util.findPattIn2DStr(lines, pattGp))
    for pattGp in (
        patt, patt[::-1],
        (patt,), (patt[::-1],),
        tuple('.' * i + c for i, c in enumerate(patt)),
        tuple('.' * i + c for i, c in enumerate(patt))[::-1],
        tuple('.' * i + c for i, c in enumerate(patt[::-1])),
        tuple('.' * i + c for i, c in enumerate(patt[::-1]))[::-1],
    )
)
print(count)


# part 2
newPatt = ('M.S', '.A.', 'M.S')
count = sum(
    len(util.findPattIn2DStr(lines, pattGp))
    for pattGp in (
        newPatt,
        tuple(''.join(r[::-1]) for r in newPatt),
        tuple(''.join(r) for r in util.transpose(newPatt)),
        tuple(''.join(r) for r in util.transpose(newPatt))[::-1],
    )
)
print(count)


