import AOCInit
import util

if __name__ != "__main__":
    exit()

inp = util.getInput(d=1, y=2025)

# part 1
init = 50
count = 0
for l in inp.splitlines():
    if l[0] == "L":
        init -= int(l[1:])
    else:
        init += int(l[1:])
    init = ((init % 100) + 100) % 100
    if init == 0:
        count += 1
print(count)


# part 2
init = 50
count = 0
atZero = False
for l in inp.splitlines():
    q, r = divmod(int(l[1:]), 100)
    if l[0] == "L":
        count += q
        init -= r
        if init < 0:
            init += 100
            count += 1
        if init == 0:
            count += 1
        if atZero:
            count -= 1
    else:
        count += q
        init += r
        if init >= 100:
            init -= 100
            count += 1
    atZero = init == 0
print(count)

