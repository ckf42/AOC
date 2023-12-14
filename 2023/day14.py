import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=14, y=2023)

graph = list(list(line) for line in inp.splitlines())
dim = (len(graph), len(graph[0]))

assert dim[0] == dim[1], "not square"
d = dim[0]

# part 1
totalSum = 0
for j in range(d):
    for i in range(d):
        if graph[i][j] != 'O':
            continue
        graph[i][j] = '.'
        newI = i
        for ii in range(i - 1, -1, -1):
            if graph[ii][j] != '.':
                break
            newI = ii
        graph[newI][j] = 'O'
        totalSum += d - newI
print(totalSum)


# part 2
graph = list(list(line) for line in inp.splitlines())

totalCyc = 1000000000
repToCyc: dict[str, int] = dict()
cycToSum = [0]
cycleDone = 0
while True:
    for _ in range(4):
        for j in range(d):
            for i in range(d):
                if graph[i][j] != 'O':
                    continue
                graph[i][j] = '.'
                for ii in range(i, 0, -1):
                    if graph[ii - 1][j] != '.':
                        graph[ii][j] = 'O'
                        break
                else:  # no break
                    graph[0][j] = 'O'
        graph = list(list(graph[d - j - 1][i]
                          for j in range(d))
                     for i in range(d))
    cycleDone += 1
    graphRep = ''.join(b for line in graph for b in line)
    if (pBegin := repToCyc.get(graphRep, None)) is not None:
        print(cycToSum[pBegin + (totalCyc - pBegin) % (cycleDone - pBegin)])
        break
    else:
        repToCyc[graphRep] = cycleDone
        cycToSum.append(sum(d - i
                            for i in range(d)
                            for j in range(d)
                            if graph[i][j] == 'O'))

