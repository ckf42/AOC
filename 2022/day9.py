import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = tuple((ls[0], int(ls[1])) for l in util.getInput(d=9, y=2022).splitlines() if (ls := l.split()))

def isTouching(h, t):
    return max(abs(h[i] - t[i]) for i in (0, 1)) <= 1

def simu(ropeLen):
    rope = list(list((0, 0)) for i in range(ropeLen))
    tailHistory = set()
    tailHistory.add(tuple(rope[-1]))
    for inst in inp:
        for count in range(inst[1]):
            # update head
            rope[0] = [rope[0][0] + {'L': -1, 'R': 1}.get(inst[0], 0),
                       rope[0][1] + {'U': 1, 'D': -1}.get(inst[0], 0)]
            # update tail
            for part in range(ropeLen - 1):
                if not isTouching(rope[part], rope[part + 1]):
                    if rope[part][0] == rope[part + 1][0]:
                        if rope[part][1] != rope[part + 1][1]:
                            rope[part + 1][1] += util.sgn(rope[part][1] - rope[part + 1][1])
                    elif rope[part][1] == rope[part + 1][1]:
                        if rope[part][0] != rope[part + 1][0]:
                            rope[part + 1][0] += util.sgn(rope[part][0] - rope[part + 1][0])
                    else:
                        # diag
                        walkMajor = (0 if abs(rope[part][0] - rope[part + 1][0]) == 2 else 1)
                        rope[part + 1][walkMajor] += util.sgn(rope[part][walkMajor]\
                                - rope[part + 1][walkMajor])
                        rope[part + 1][1 - walkMajor] += util.sgn(rope[part][1 - walkMajor]\
                                - rope[part + 1][1 - walkMajor])
            tailHistory.add(tuple(rope[-1]))
    return len(tailHistory)

# part 1
print(simu(2))

# part 2
print(simu(10))

