import AOCInit
import util
import heapq as hq

if __name__ != '__main__':
    exit()

inp = util.getInput(d=12, y=2022)
startLoc = inp.find('S')
endLoc = inp.find('E')
inp = inp.splitlines()
dim = (len(inp), len(inp[0]))
startLoc = divmod(startLoc, dim[1] + 1) # +1 for newline
endLoc = divmod(endLoc, dim[1] + 1)
dirList = ((1, 0), (0, 1), (-1, 0), (0, -1))

def elev(p):
    c = inp[p[0]][p[1]]
    return {'S': 0, 'E': 25}.get(c, ord(c) - ord('a'))

# part 1
costFunc = lambda n, o, c: c + 1
neiLstFunc = lambda n: tuple(nd
                             for d in dirList
                             if (nd := tuple(n[i] + d[i] for i in range(2))) \
                                and all(0 <= nd[i] < dim[i] for i in range(2)) \
                                and elev(n) + 1 >= elev(nd))
isGoal = lambda n: n == endLoc
aStar = lambda n: sum(abs(n[i] - endLoc[i]) for i in range(2))
print(util.bfs(initialNode=startLoc,
               costFunc=costFunc,
               neighbourListFunc=neiLstFunc,
               goalCheckerFunc=isGoal,
               aStarHeuristicFunc=aStar)[1])

# part 2
neiLstFunc = lambda n: tuple(nd
                             for d in dirList
                             if (nd := tuple(n[i] + d[i] for i in range(2))) \
                                and all(0 <= nd[i] < dim[i] for i in range(2)) \
                                and elev(n) <= 1 + elev(nd))
isGoal = lambda n: elev(n) == 0
print(util.bfs(initialNode=endLoc,
               costFunc=costFunc,
               neighbourListFunc=neiLstFunc,
               goalCheckerFunc=isGoal)[1])

