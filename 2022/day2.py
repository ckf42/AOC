import util

inp = util.getInput(d=2)
lineArr = inp.split('\n')[:-1]
arr = list(l.split() for l in lineArr)

winOrder = 'ACB'
shapePtDict = {'A': 1, 'B': 2, 'C': 3}

# part 1
def rps1(c1, c2):
    transDict = {'X': 'A', 'Y': 'B', 'Z': 'C'}
    c2 = transDict[c2]
    shapePt = shapePtDict[c2]
    winLosePt = list(i for i in range(-1, 2) if winOrder[(winOrder.find(c2) + i) % 3] == c1)[0]
    gamePt = 3 * (1 + winLosePt)
    return shapePt + gamePt

print(sum(rps1(p[0], p[1]) for p in arr))


# part 2
def rps2(c1, c2):
    gameDict = {'X': -1, 'Y': 0, 'Z': 1}
    gamePt = (gameDict[c2] + 1) * 3
    shapePt = shapePtDict[winOrder[(winOrder.find(c1) - gameDict[c2]) % 3]]
    return gamePt + shapePt

print(sum(rps2(p[0], p[1]) for p in arr))

