import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = """\
5-8
0-2
4-7\
"""
inp = util.getInput(d=20, y=2016)

ipList = tuple(util.getInts(l, allowNegative=False) for l in inp.splitlines())

# part 1
itvColl = util.IntegerIntervals(*ipList)
comp0 = itvColl[0]
if comp0[0] != 0:
    print(0)
else:
    print(comp0[1] + 1)

# part 2
highest = 4294967295
print(highest + 1 - len(itvColl))

