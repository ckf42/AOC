import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=4, y=2022).splitlines()
arr = list(util.splitIntoGp(util.getInts(l), 2) for l in inp)

# part 1
def isCountain(c1, c2):
    return (c1[0] <= c2[0] and c2[1] <= c1[1]) \
            or (c2[0] <= c1[0] and c1[1] <= c2[1])

print(sum(isCountain(*p) for p in arr))

# part 2
def isOverlap(c1, c2):
    return (c1[0] <= c2[0] <= c1[1]) \
            or (c1[0] <= c2[1] <= c1[1]) \
            or (c2[0] <= c1[0] <= c2[1]) \
            or (c2[0] <= c1[1] <= c2[1])

print(sum(isOverlap(*p) for p in arr))

