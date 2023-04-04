import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = """\
1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc\
"""
inp = util.getInput(d=2, y=2020)

corpList = tuple(
        (
            util.getInts(line, allowNegative=False),
            line.split(maxsplit=2)[1][:-1],
            line.rsplit(maxsplit=1)[-1]
        )
        for line in inp.splitlines()
)

# part 1
counter = 0
for (r, c, s) in corpList:
    if util.countItem(s, c) in range(r[0], r[1] + 1):
        counter += 1
print(counter)

# part 2
counter = 0
for (r, c, s) in corpList:
    if (s[r[0] - 1] == c) ^ (s[r[1] - 1] == c):
        counter += 1
print(counter)


