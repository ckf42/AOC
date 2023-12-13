import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=13, y=2023)

patterns = tuple(patt.splitlines() for patt in inp.split('\n\n'))

# part 1
def findMirrorRow(patt, targetDiff=0):
    for i in range(len(patt) - 1):  # last row idx on top
        if sum(a != b
               for r in range(max(0, 2 * i + 2 - len(patt)), i + 1)
               for a, b in zip(patt[r], patt[2 * i + 1 - r])) == targetDiff:
            return i + 1
    return -1

totalSum = 0
for patt in patterns:
    res = findMirrorRow(patt)
    if res != -1:
        res *= 100
    else:
        res = findMirrorRow(util.transpose(patt))
    totalSum += res
print(totalSum)

# part 2
totalSum = 0
for patt in patterns:
    res = findMirrorRow(patt, 1)
    if res != -1:
        res *= 100
    else:
        res = findMirrorRow(util.transpose(patt), 1)
    totalSum += res
print(totalSum)



