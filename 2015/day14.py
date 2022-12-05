import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=14, y=2015).splitlines()
# timeElasp = 2503
timeElasp = 1000
# deerArr = list((l.split(maxsplit=1)[0], util.getInts(l)) for l in inp)
deerArr = [
    ('Comet', (14, 10, 127)),
    ('Dancer', (16, 11, 162)),
]

# part 1
def dist(s):
    d, m = divmod(timeElasp, s[1][1] + s[1][2])
    return (d * s[1][1] + min(m, s[1][1])) * s[1][0]

print(dist(max(deerArr, key=dist)))

# part 2
# ?
