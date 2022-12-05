import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=5, y=2022).splitlines()
sep = inp.index('')
stackGraph = list(util.takeFromEvery(l, 4, 1) for l in inp[:sep])
stackList = list(list(filter(lambda x: x != ' ',
                             tuple(s[i] for s in stackGraph)))[::-1]
                 for i in range(9))
instructions = tuple(util.getInts(l) for l in inp[sep + 1:])

# part 1
newStackList = list(s[:] for s in stackList)
for inst in instructions:
    (newStackList[inst[1] - 1], sl) = util.splitAt(newStackList[inst[1] - 1], -inst[0])
    newStackList[inst[2] - 1] += sl[::-1]
print(''.join(map(lambda s: s[-1], newStackList)))

# part 2
newStackList = list(s[:] for s in stackList)
for inst in instructions:
    (newStackList[inst[1] - 1], sl) = util.splitAt(newStackList[inst[1] - 1], -inst[0])
    newStackList[inst[2] - 1] += sl
print(''.join(map(lambda s: s[-1], newStackList)))

