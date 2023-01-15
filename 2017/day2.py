import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=2, y=2017)
sheetLine = tuple(util.getInts(l) for l in inp.splitlines())

# part 1
print(sum(p[1] - p[0] for p in util.rangeBound(sheetLine)))

# part 2
def findDivisibleRatio(seq):
    for i in range(len(seq) - 1):
        for j in range(i + 1, len(seq)):
            (p, q) = (seq[i], seq[j])
            if q > p:
                (p, q) = (q, p)
            (r, m) = divmod(p, q)
            if m == 0:
                return r

print(sum(findDivisibleRatio(l) for l in sheetLine))

