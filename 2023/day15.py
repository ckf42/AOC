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
# 3.7+ dict preserve insert order
boxes: list[dict[str, int]] = list(dict() for _ in range(256))
for inst in instLines:
    if inst[-1] == '-':
        label = inst[:-1]
        bIdx = h(label)
        try:
            boxes[bIdx].pop(label)
        except KeyError:
            pass
    else:
        label = inst[:-2]
        focalLen = int(inst[-1])
        bIdx = h(label)
        boxes[bIdx][label] = focalLen
print(sum(boxIdx * lenIdx * focalLen
          for boxIdx, box in enumerate(boxes, start=1)
          for lenIdx, focalLen in enumerate(box.values(), start=1)))

