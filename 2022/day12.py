import AOCInit
import util
import heapq as hq

if __name__ != '__main__':
    exit()

inp = util.getInput(d=12, y=2022)
startLoc = inp.find('S')
endLoc = inp.find('E')
inp = inp.splitlines()
d = (len(inp), len(inp[0]))
startLoc = divmod(startLoc, d[1] + 1) # newline
endLoc = divmod(endLoc, d[1] + 1)
dirList = ((1, 0), (0, 1), (-1, 0), (0, -1))

def elev(p):
    c = inp[p[0]][p[1]]
    return {'S': 0, 'E': 25}.get(c, ord(c) - ord('a'))

# part 1
h = list()
visited = set()
h.append((0, startLoc))
while len(h) != 0:
    top = hq.heappop(h)
    if top[1] == endLoc:
        print(top[0])
        break
    elif top[1] in visited:
        continue
    else:
        visited.add(top[1])
        for direction in dirList:
            newDir = tuple(top[1][i] + direction[i] for i in range(2))
            if all(0 <= newDir[idx] < d[idx] for idx in range(2)) \
                    and elev(top[1]) + 1 >= elev(newDir):
                hq.heappush(h, (top[0] + 1, newDir))




# part 2
h = list()
visited = set()
h.append((0, endLoc))
while len(h) != 0:
    top = hq.heappop(h)
    if elev(top[1]) == 0:
        print(top[0])
        break
    elif top[1] in visited:
        continue
    else:
        visited.add(top[1])
        for direction in dirList:
            newDir = tuple(top[1][i] + direction[i] for i in range(2))
            if all(0 <= newDir[idx] < d[idx] for idx in range(2)) \
                    and elev(top[1]) <= 1 + elev(newDir):
                hq.heappush(h, (top[0] + 1 , newDir))

