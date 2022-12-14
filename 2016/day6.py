import AOCInit
import util
from collections import Counter

if __name__ != '__main__':
    exit()

inp = util.transpose(util.getInput(d=6, y=2016).splitlines())
countList = tuple(Counter(p) for p in inp)

# part 1
print(''.join(c.most_common(1)[0][0] for c in countList))

# part 2
print(''.join(c.most_common()[-1][0] for c in countList))


