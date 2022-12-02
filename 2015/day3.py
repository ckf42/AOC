import AOCInit
import util

inp = util.getInput(d=3, y=2015)

# part 1
visited = set()
currLoc = (0, 0)

def moveLoc(curr, direction):
    return (curr[0] + {'>': 1, '<': -1}.get(direction, 0),
            curr[1] + {'^': 1, 'v': -1}.get(direction, 0))

visited.add(currLoc)
for ind in inp:
    currLoc = moveLoc(currLoc, ind)
    visited.add(currLoc)
print(len(visited))

# part 2
visited.clear()
inpl = len(inp)
currLoc = (0, 0)
for i in range(0, inpl, 2):
    currLoc = moveLoc(currLoc, inp[i])
    visited.add(currLoc)
currLoc = (0, 0)
for i in range(1, inpl, 2):
    currLoc = moveLoc(currLoc, inp[i])
    visited.add(currLoc)
print(len(visited))

