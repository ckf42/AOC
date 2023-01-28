import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = """\
pos=<0,0,0>, r=4
pos=<1,0,0>, r=1
pos=<4,0,0>, r=3
pos=<0,2,0>, r=1
pos=<0,5,0>, r=3
pos=<0,0,3>, r=1
pos=<1,1,1>, r=1
pos=<1,1,2>, r=1
pos=<1,3,1>, r=1\
"""
inp = util.getInput(d=23, y=2018)

botList = tuple((util.Point(*ls[:3]), ls[3])
                for l in inp.splitlines()
                if (ls := util.getInts(l)))

# part 1
sBotIdx = util.argmax(range(len(botList)),
                      lambda idx: botList[idx][1])
print(util.count(botList,
                 lambda botSp: (botSp[0] - botList[sBotIdx][0]).norm(1) <= botList[sBotIdx][1]))


# part 2


