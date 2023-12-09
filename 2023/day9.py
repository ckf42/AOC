import AOCInit
import util
from itertools import accumulate

if __name__ != '__main__':
    exit()

inp = util.getInput(d=9, y=2023)

histories = tuple(util.getInts(line) for line in inp.splitlines())

def getSeeds(seq):
    seeds = list()
    while any(x != 0 for x in seq):
        seeds.append(seq[0])
        seq = util.diff(seq)
    return seeds
historySeeds = tuple(getSeeds(h) for h in histories)

# part 1
# math sol probably gives blown up coeff in the polynomial
def getNextTerm(seeds, n):
    seq = (seeds[-1],) * (n - len(seeds) + 2)
    for s in seeds[-2::-1]:
        seq = tuple(accumulate(seq, initial=s))
    return seq[-1]

print(sum(getNextTerm(s, l)
          for s, l in zip(historySeeds,
                          (len(h) for h in histories))))

# part 2
def getPrevTerm(seeds):
    head = 0
    for s in seeds[::-1]:
        head = s - head
    return head

print(sum(getPrevTerm(s) for s in historySeeds))


