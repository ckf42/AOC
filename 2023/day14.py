import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=14, y=2023)

graph: list[str] = inp.splitlines()
dim = (len(graph), len(graph[0]))

assert dim[0] == dim[1], "not square"
d = dim[0]

for i in range(d // 2):
    graph[i], graph[d - 1 - i] = graph[d - 1 - i], graph[i]
graph = list(''.join(line) for line in zip(*graph))

# part 1
for i in range(d):
    graph[i] = '#'.join(
            '.' * c + 'O' * (len(seg) - c)
            for seg in graph[i].split('#')
            if (c := seg.count('.')) or True)
print(sum(j + 1
          for line in graph
          for j in range(d)
          if line[j] == 'O'))


# part 2
graph = inp.splitlines()
for i in range(d // 2):
    graph[i], graph[d - 1 - i] = graph[d - 1 - i], graph[i]
graph = list(''.join(line) for line in zip(*graph))

totalCyc = 1000000000
repToCyc: dict[str, int] = dict()
cycToSum = [0]
cycleDone = 0
while True:
    for _ in range(4):
        for i in range(d):
            # ~60% of time is spent here. Optimize?
            graph[i] = '#'.join(
                    '.' * c + 'O' * (len(seg) - c)
                    for seg in graph[i].split('#')
                    if (c := seg.count('.')) or True)
        # even faster rotation?
        for i in range(d // 2):
            graph[i], graph[d - 1 - i] = graph[d - 1 - i], graph[i]
        graph = list(''.join(line) for line in zip(*graph))
    cycleDone += 1
    graphRep = ''.join(line for line in graph)
    if (pBegin := repToCyc.get(graphRep, None)) is not None:
        print(cycToSum[pBegin + (totalCyc - pBegin) % (cycleDone - pBegin)])
        break
    else:
        repToCyc[graphRep] = cycleDone
        # ~33% of time spent here. Optimize?
        cycToSum.append(sum(j + 1
                            for line in graph
                            for j in range(d)
                            if line[j] == 'O'))

