import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=4, y=2024)

lines = inp.splitlines()
n = len(lines)
m = len(lines[0])  # assume rect

# part 1
count = sum(
    len(util.findPattIn2DStr(lines, pattGp))
    for pattGp in (
        'XMAS', 'XMAS'[::-1],
        ('XMAS',), ('XMAS'[::-1],),
        ('X', '.M', '..A', '...S'),
        ('X', '.M', '..A', '...S')[::-1],
        ('S', '.A', '..M', '...X'),
        ('S', '.A', '..M', '...X')[::-1],
    )
)
print(count)


# part 2
count = sum(
    len(util.findPattIn2DStr(lines, pattGp))
    for pattGp in (
        ('M.S', '.A.', 'M.S'),
        tuple(r[::-1] for r in ('M.S', '.A.', 'M.S')),
        ('S.S', '.A.', 'M.M'),
        ('S.S', '.A.', 'M.M')[::-1]
    )
)
print(count)


