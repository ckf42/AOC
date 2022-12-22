import AOCInit
import util
import re
from collections import deque

if __name__ != '__main__':
    exit()

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

inp = util.getInput(d=22, y=2022)

board = inp.splitlines()[:-2]
maxCol = max(len(l) for l in board)
board = tuple(l + ' ' * (maxCol - len(l))
              for l in board)
pathDesc = re.findall(r'(\d+|[LR])', inp.splitlines()[-1])
direction = ((1, 0), (0, 1), (-1, 0), (0, -1)) # L <- -> R
dim = (len(board[0]), len(board))

# part 1
# currLoc = (util.firstIdxSuchThat(board[0], lambda c: c == '.'), 0)
# faceDir = 0
# for inst in pathDesc:
    # if inst.isdigit():
        # d = direction[faceDir]
        # for _ in range(int(inst)):
            # nextLoc = tuple((currLoc[i] + d[i]) % dim[i] for i in range(2))
            # while board[nextLoc[1]][nextLoc[0]] not in '.#':
                # nextLoc = tuple((nextLoc[i] + d[i]) % dim[i] for i in range(2))
            # if board[nextLoc[1]][nextLoc[0]] == '.':
                # currLoc = nextLoc
            # else:
                # break
    # else:
        # faceDir = (faceDir + {'L': -1, 'R': 1}[inst]) % 4
# print((currLoc[0] + 1) * 4 + (currLoc[1] + 1) * 1000 + faceDir)

# part 2
faceLen = util.gcd(max(util.count(l, lambda c: c != ' '))
                   for l in board)
# index:
#  1
# 402
#  3
#  5
# mapping: index in anchorPt reg
# direction: number of right rotation deviated from canonical (1, 0)
# canonical: 0, 5: point right, 1:4: outward
orient = list([None, 0] for _ in range(6))

def rotRight(changeDir):
    # rot vect points inward
    orient[1:5] = orient[2:5] + orient[1:2]
    if changeDir:
        orient[0][1] = (orient[0][1] + 1) % 4
        orient[0][5] = (orient[0][5] + 1) % 4

def rotLeft(changeDir):
    # rot vect points outward
    orient[1:5] = orient[4:5] + orient[1:4]
    if changeDir:
        orient[0][1] = (orient[0][1] - 1) % 4
        orient[0][5] = (orient[0][5] - 1) % 4

def goUp(changeDir):
    # go pass top edge
    orient[1], orient[0], orient[3], orient[5] = orient[5], orient[1], orient[0], orient[3]
    if changeDir:
        orient[2][1] = (orient[2][1] - 1) % 4
        orient[4][1] = (orient[4][1] + 1) % 4


searchPt = (util.firstIdxSuchThat(board[0], lambda c: c == '.'), 0) # face 0
visited = set()
q = deque((searchPt,))
while len(q) != 0:
    pt = q.popleft()
    if pt in visited:
        continue
    # right
    newPt = (pt[0] + faceLen, pt[1])
    if all(0 <= newPt[i] < dim[i] for i in range(2)) \
            and board[newPt[1]][newPt[0]] != ' ':
        # is a face




