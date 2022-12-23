import AOCInit
import util
import re

if __name__ != '__main__':
    exit()

# test case
inp = \
"""        ...#    
        .#..    
        #...    
        ....    
...#.......#    
........#...    
..#....#....    
..........#.    
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5"""

# inp = util.getInput(d=22, y=2022)

board = inp.splitlines()[:-2]
maxCol = max(len(l) for l in board)
board = tuple(l + ' ' * (maxCol - len(l))
              for l in board)
pathDesc = re.findall(r'(\d+|[LR])', inp.splitlines()[-1])
direction = ((1, 0), (0, 1), (-1, 0), (0, -1)) # L <- -> R
dim = (len(board[0]), len(board))

# part 1
currLoc = (util.firstIdxSuchThat(board[0], lambda c: c == '.'), 0)
faceDir = 0
for inst in pathDesc:
    if inst.isdigit():
        d = direction[faceDir]
        for _ in range(int(inst)):
            nextLoc = tuple((currLoc[i] + d[i]) % dim[i] for i in range(2))
            while board[nextLoc[1]][nextLoc[0]] not in '.#':
                nextLoc = tuple((nextLoc[i] + d[i]) % dim[i] for i in range(2))
            if board[nextLoc[1]][nextLoc[0]] == '.':
                currLoc = nextLoc
            else:
                break
    else:
        faceDir = (faceDir + {'L': -1, 'R': 1}[inst]) % 4
print((currLoc[0] + 1) * 4 + (currLoc[1] + 1) * 1000 + faceDir)

# part 2
faceLen = util.gcd(*(util.count(l, lambda c: c != ' ') for l in board))
# index:
#  1
# 402
#  3
#  5
# anchorPt: upper-left coor in 2D map
# direction: number of right rotation of precepted (1, 0) deviated from 2D map (1, 0)
orient = list([None, 0] for _ in range(6))

def rotRight():
    # rot vect points inward
    orient[1:5] = orient[2:5] + orient[1:2]
    orient[0][1] = (orient[0][1] - 1) % 4
    orient[5][1] = (orient[5][1] + 1) % 4

def shiftUp():
    # go pass top edge, rot vect points right
    orient[1], orient[0], orient[3], orient[5] = orient[5], orient[1], orient[0], orient[3]
    orient[2][1] = (orient[2][1] - 1) % 4
    orient[4][1] = (orient[4][1] + 1) % 4

def rotLeft():
    # rot vect points outward
    rotRight()
    rotRight()
    rotRight()

def shiftDown():
    shiftUp()
    shiftUp()
    shiftUp()

def shiftRight():
    # point down
    rotRight()
    shiftUp()
    rotLeft()

# TODO: find out why rotLeft(); shiftUp(); rotRight() does not give correct shiftLeft
def shiftLeft():
    shiftRight()
    shiftRight()
    shiftRight()

def shiftLeftOther():
    rotLeft()
    shiftUp()
    rotRight()

searchPt = (util.firstIdxSuchThat(board[0], lambda c: c == '.'), 0) # face 0
visited = set()

def registerFace(pt):
    orient[0] = [pt, 0]
    visited.add(pt)
    for d, md in (((1, 0), 'r'), ((0, 1), 'd'), ((-1, 0), 'l'), ((0, -1), 'u')):
        newPt = tuple(pt[i] + d[i] * faceLen for i in range(2))
        if newPt not in visited \
                and all(0 <= newPt[i] < dim[i] for i in range(2)) \
                and board[newPt[1]][newPt[0]] != ' ':
            if md == 'r':
                shiftRight()
                registerFace(newPt)
                shiftLeft()
            elif md == 'd':
                shiftDown()
                registerFace(newPt)
                shiftUp()
            elif md == 'l':
                shiftLeft()
                registerFace(newPt)
                shiftRight()
            else:
                shiftUp()
                registerFace(newPt)
                shiftDown()

registerFace(searchPt)

def preceptTofaceCoor(pt, deviate):
    for _ in range(deviate):
        pt = (pt[1], faceLen - 1 - pt[0])
    return pt

realLoc = (util.firstIdxSuchThat(board[0], lambda c: c == '.'), 0) # coor on 2D map
preceptLoc = (0, 0) # coor on surface 0
preceptFaceDir = 0

def printBoard():
    for y in range(dim[1]):
        for x in range(dim[0]):
            if (x, y) == realLoc:
                print('x', end='')
            else:
                print(board[y][x], end='')
        print('')

# printBoard()
for inst in pathDesc:
    if inst.isdigit():
        d = direction[preceptFaceDir]
        for _ in range(int(inst)):
            preceptNextLoc = tuple(preceptLoc[i] + d[i] for i in range(2))
            rotatedAction = None
            if preceptNextLoc[0] < 0:
                shiftLeft()
                rotatedAction = 'l'
                preceptNextLoc = (faceLen - 1, preceptNextLoc[1])
            elif preceptNextLoc[0] == faceLen:
                shiftRight()
                rotatedAction = 'r'
                preceptNextLoc = (0, preceptNextLoc[1])
            elif preceptNextLoc[1] < 0:
                shiftUp()
                rotatedAction = 'u'
                preceptNextLoc = (preceptNextLoc[0], faceLen - 1)
            elif preceptNextLoc[1] == faceLen:
                shiftDown()
                rotatedAction = 'd'
                preceptNextLoc = (preceptNextLoc[0], 0)
            faceCoor = preceptTofaceCoor(preceptNextLoc, orient[0][1])
            realNextLoc = tuple(orient[0][0][i] + faceCoor[i] for i in range(2))
            if board[realNextLoc[1]][realNextLoc[0]] == '.':
                realLoc = realNextLoc
                preceptLoc = preceptNextLoc
            else:
                if rotatedAction is not None:
                    {'l': shiftRight, 'r': shiftLeft, 'u': shiftDown, 'd': shiftUp}[rotatedAction]()
                break
    else:
        preceptFaceDir = (preceptFaceDir + {'L': -1, 'R': 1}[inst]) % 4
    # print(inst, '>v<^'[(preceptFaceDir - orient[0][1]) % 4])
    # printBoard()
print((realLoc[0] + 1) * 4 + (realLoc[1] + 1) * 1000 + (preceptFaceDir - orient[0][1]) % 4)

