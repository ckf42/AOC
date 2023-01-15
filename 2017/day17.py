import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=17, y=2017)
skipSize = int(inp)

# part 1
buff = [0]
currPos = 0
for i in range(1, 2017 + 1):
    currPos = (currPos + skipSize) % i + 1
    buff.insert(currPos, i)
print(util.cycInd(buff, currPos + 1))


# part 2
# TODO: takes ~17s
zeroPos = 0
followEle = None
currPos = 0
for i in range(1, 50000000 + 1):
    currPos = (currPos + skipSize) % i + 1
    if currPos == zeroPos + 1:
        followEle = i
print(followEle)


