import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=2, y=2021)
instructions = tuple(
    (line.split()[0], int(line.split()[1]))
    for line in inp.splitlines()
)

# part 1
x, y = 0, 0
for (inst, arg) in instructions:
    if inst == 'forward':
        x += arg
    elif inst == 'down':
        y += arg
    else:
        # up
        y -= arg
print(x * y)

# part 2
x, y = 0, 0
aim = 0
for (inst, arg) in instructions:
    if inst == 'forward':
        x += arg
        y += aim * arg
    elif inst == 'down':
        aim += arg
    else:
        # up
        aim -= arg
print(x * y)

