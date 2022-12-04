import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=2, y=2022).splitlines()
arr = list(l.split() for l in inp)

winOrder = 'ACB'
shapePtDict = {'A': 1, 'B': 2, 'C': 3}

# part 1
transDict = {'X': 'A', 'Y': 'B', 'Z': 'C'}

def rps1(c1, c2):
    c2 = transDict[c2]
    shapePt = shapePtDict[c2]
    i2 = winOrder.find(c2)
    winLosePt = util.firstSuchThat(range(-1, 2),
                                   lambda i: util.cycInd(winOrder, i2 + i) == c1)[1]
    gamePt = 3 * (1 + winLosePt)
    return shapePt + gamePt

print(sum(rps1(*p) for p in arr))

# part 2
gameDict = {'X': -1, 'Y': 0, 'Z': 1}

def rps2(c1, c2):
    gamePt = (gameDict[c2] + 1) * 3
    shapePt = shapePtDict[util.cycInd(winOrder, winOrder.find(c1) - gameDict[c2])]
    return gamePt + shapePt

print(sum(rps2(*p) for p in arr))

