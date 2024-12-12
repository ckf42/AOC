import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=11, y=2024)

nums = util.getInts(inp)

cache: dict[tuple[int, int], int] = dict()

def tryEval(buff: list[tuple[int, int]]) -> None:
    while len(buff) != 0:
        x, count = buff[-1]
        if (x, count) in cache:
            buff.pop()
        elif count == 0:
            cache[(x, 0)] = 1
            buff.pop()
        elif x == 0:
            if (1, count - 1) not in cache:
                buff.append((1, count - 1))
            else:
                cache[(0, count)] = cache[(1, count - 1)]
                buff.pop()
        elif len(s := str(x)) & 1:
            if (x * 2024, count - 1) not in cache:
                buff.append((x * 2024, count - 1))
            else:
                cache[(x, count)] = cache[(x * 2024, count - 1)]
                buff.pop()
        else:
            a = int(s[:len(s) // 2])
            b = int(s[len(s) // 2:])
            uneval = False
            for y in (a, b):
                if (y, count - 1) not in cache:
                    uneval = True
                    buff.append((y, count - 1))
            if not uneval:
                cache[(x, count)] = sum(cache[(y, count - 1)] for y in (a, b))
                buff.pop()

# part 1
timer = util.Timer()
tryEval([(x, 25) for x in nums])
print(sum(cache[(x, 25)] for x in nums))
timer.check()

# part 2
tryEval([(x, 75) for x in nums])
print(sum(cache[(x, 75)] for x in nums))
timer.check()

for t in (100, 500, 1000, 10000):
    tryEval([(x, t) for x in nums])
    print(sum(cache[(x, t)] for x in nums))
    timer.check()
timer.stop()

