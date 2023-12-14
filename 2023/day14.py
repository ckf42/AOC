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
    nextSpot = 0
    for i in range(d):
        c = graph[i][j]
        if c == '.':
            continue
        if c == 'O':
            graph[i][j] = '.'
            graph[nextSpot][j] = 'O'
            totalSum += d - nextSpot
            nextSpot += 1
        else:
            nextSpot = i + 1
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
            nextSpot = 0
            # ~25% of time is spent here. Can we optimize this part?
            for i in range(d):
                # does not seem much faster than nested if
                match graph[i][j]:
                    case '.':
                        continue
                    case 'O':
                        graph[i][j] = '.'
                        graph[nextSpot][j] = 'O'
                        nextSpot += 1
                    case _:
                        nextSpot = i + 1
        # even faster rotation?
        for i in range(d // 2):
            graph[i], graph[d - 1 - i] = graph[d - 1 - i], graph[i]
        graph = list(list(line) for line in zip(*graph))
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

