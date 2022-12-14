import AOCInit
import util

if __name__ != '__main__':
    exit()

edgeList = tuple(util.getInts(l) for l in util.getInput(d=3, y=2016).splitlines())

# part 1
print(util.count(edgeList, lambda p: sum(p) > 2 * max(p)))

# part 2
edgeList = util.flatten(util.splitIntoGp(l, 3) for l in util.transpose(edgeList))
print(util.count(edgeList, lambda p: sum(p) > 2 * max(p)))


