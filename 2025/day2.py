import AOCInit
import util
import re

if __name__ != "__main__":
    exit()


inp = util.getInput(d=2, y=2025)


# part 1
def isInvalid(x: int) -> bool:
    s = str(x)
    return (len(s) & 1) == 0 and s[: len(s) // 2] == s[len(s) // 2 :]


total = 0
for part in inp.split(","):
    a, b = (int(x) for x in part.split("-"))
    for i in range(a, b + 1):
        if isInvalid(i):
            total += i
print(total)


# part 2
patt = re.compile(r"^(.+)\1+$")
total = 0
for part in inp.split(","):
    a, b = (int(x) for x in part.split("-"))
    for i in range(a, b + 1):
        if patt.match(str(i)):
            total += i
print(total)
