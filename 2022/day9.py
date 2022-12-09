import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = tuple((ls[0], int(ls[1]))
            for l in util.getInput(d=9, y=2022).splitlines()
            if (ls := l.split()))

def isTouching(h, t):
    return max(abs(h[i] - t[i]) for i in (0, 1)) <= 1

def simu(ropeLen):
    rope = list([0, 0] for i in range(ropeLen))
    tailHistory = set()
    tailHistory.add(tuple(rope[-1]))
    for inst in inp:
        moveDist = ({'L': -1, 'R': 1}.get(inst[0], 0),
                    {'U': 1, 'D': -1}.get(inst[0], 0))
        for count in range(inst[1]):
            # update head
            for d in (0, 1):
                rope[0][d] += moveDist[d]
            # update tail
            for part in range(ropeLen - 1):
                if not isTouching(rope[part], rope[part + 1]):
                    for d in (0, 1):
                        rope[part + 1][d] += util.sgn(rope[part][d] - rope[part + 1][d])
                else:
                    # no need to move remain parts
                    break
            tailHistory.add(tuple(rope[-1]))
    return len(tailHistory)

# part 1
print(simu(2))

# part 2
print(simu(10))

