import AOCInit
import util
from collections import defaultdict

if __name__ != "__main__":
    exit()


inp = util.getInput(d=11, y=2025)

edges = defaultdict(list)
backEdges = defaultdict(list)
for line in inp.splitlines():
    dev = line.split(":", maxsplit=1)[0]
    outs = line.split(":", maxsplit=1)[1].strip().split()
    for o in outs:
        edges[dev].append(o)
        backEdges[o].append(dev)


# part 1
def countPaths(source, target):
    def dfs(node, count):
        count[node] += 1
        if node == target:
            return
        for o in edges[node]:
            dfs(o, count)

    count = defaultdict(int)
    dfs(source, count)
    return count[target]


print(countPaths("you", "out"))

# part 2


def canReach(source, target):
    visited = set()
    buff = [source]
    while len(buff) != 0:
        node = buff.pop()
        if node == target:
            return True
        if node in visited:
            continue
        visited.add(node)
        for o in edges[node]:
            buff.append(o)
    return False


def canReachTo(target):
    visited = set()
    buff = [target]
    while len(buff) != 0:
        node = buff.pop()
        if node in visited:
            continue
        visited.add(node)
        for o in backEdges[node]:
            buff.append(o)
    return visited


canReachToFFT = canReachTo("fft")
canReachToDAC = canReachTo("dac")

assert "fft" in canReachToDAC
assert "dac" not in canReachToFFT


def countPathsPermit(source, target, permitSet):
    def dfs(node, count):
        count[node] += 1
        if node == target:
            return
        for o in edges[node]:
            if o in permitSet:
                dfs(o, count)

    count = defaultdict(int)
    dfs(source, count)
    return count[target]


print(
    countPathsPermit("svr", "fft", canReachToFFT)
    * countPathsPermit("fft", "dac", canReachToDAC)
    * countPathsPermit("dac", "out", set(edges) | set(["out"]))
)
