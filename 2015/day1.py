import AOCInit
import util

inp = util.getInput(d=1, y=2015)
seq = util.sub('()', (1, -1), inp)

# part 1
print(sum(seq))

# part 2
print(util.firstAccumSuchThat(seq, lambda x, y: x + y, lambda x: x < 0)[0] + 1)

