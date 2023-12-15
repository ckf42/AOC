import AOCInit
import util
from functools import cache

if __name__ != '__main__':
    exit()

inp = util.getInput(d=15, y=2023)

instLines = inp.strip().split(',')

# part 1
@cache
def h(s):
    cv = 0
    for c in s:
        cv += ord(c)
        cv += (cv << 4)
        cv &= 255
    return cv

print(sum(h(inst) for inst in instLines))


# part 2
boxes: list[list[tuple[str, int]]] = list(list() for _ in range(256))
for inst in instLines:
    if '=' in inst:
        label = inst[:-2]
        focalLen = int(inst[-1])
        bIdx = h(label)
        try:
            boxes[bIdx][tuple(p[0] for p in boxes[bIdx]).index(label)] \
                    = (label, focalLen)
        except ValueError:
            boxes[bIdx].append((label, focalLen))
    else:
        label = inst[:-1]
        bIdx = h(label)
        boxes[bIdx] = list((lb, f) for lb, f in boxes[bIdx] if lb != label)
totalPower = 0
for boxIdx, b in enumerate(boxes, start=1):
    for (lenIdx, (_, f)) in enumerate(b, start=1):
        totalPower += boxIdx * lenIdx * f
print(totalPower)

