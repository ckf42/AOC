import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = """\
position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>\
"""
inp = util.getInput(d=10, y=2018)

pointList = tuple([complex(ls[0], ls[1]), complex(ls[2], ls[3])]
                  for l in inp.splitlines()
                  if (ls := util.getInts(l)))
l = len(pointList)

# part 1
turn = 0
while True:
    turn += 1
    for i in range(l):
        pointList[i][0] += pointList[i][1]
    pointTuple = tuple(map(lambda p: (int(p[0].real), int(p[0].imag)), pointList))
    pointSet = frozenset(pointTuple)
    bdBox = util.rangeBound(util.transpose(pointTuple))
    if sum(map(lambda p: p[1] - p[0], bdBox)) < 80:
        for j in range(bdBox[1][0], bdBox[1][1] + 1):
            for i in range(bdBox[0][0], bdBox[0][1] + 1):
                print(util.consoleChar((i, j) in pointSet), end='')
            print('')
        print('')
        break

# part 2
print(turn)
