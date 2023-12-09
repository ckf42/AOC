import AOCInit
import util
from itertools import accumulate

if __name__ != '__main__':
    exit()

inp = util.getInput(d=9, y=2023)
histories = tuple(util.getInts(line) for line in inp.splitlines())

# part 1
# math sol probably gives blown up coeff in the polynomial
def getPrevTerm(seq):
    seeds = list()
    while any(x != 0 for x in seq):
        seeds.append(seq[0])
        seq = util.diff(seq)
    head = 0
    for s in seeds[::-1]:
        head = s - head
    return head

print(sum(getPrevTerm(seq[::-1]) for seq in histories))

# part 2
print(sum(getPrevTerm(seq) for seq in histories))


