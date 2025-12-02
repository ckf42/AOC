import AOCInit
import util

if __name__ != "__main__":
    exit()

inp = util.getInput(d=1, y=2025)

# part 1
pos = 50
count = 0
for l in inp.splitlines():
    move = int(l[1:]) % 100
    if l[0] == "L":
        pos = (pos + 100 - move) % 100
    else:
        pos = (pos + move) % 100
    if pos == 0:
        count += 1
print(count)


# part 2
pos = 50
count = 0
for l in inp.splitlines():
    q, r = divmod(int(l[1:]), 100)
    count += q
    if l[0] == "L":
        if pos == 0:
            count -= 1
        pos -= r
        if pos < 0:
            pos += 100
            count += 1
        elif pos == 0:
            count += 1
    else:
        pos += r
        if pos >= 100:
            pos -= 100
            count += 1
print(count)

