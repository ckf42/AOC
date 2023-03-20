import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=2, y=2019)

prog = list(util.getInts(inp))

# part 1
prog[1] = 12
prog[2] = 2
ptr = 0
while prog[ptr] != 99:
    assert prog[ptr] in (1, 2)
    progCode = tuple(prog[ptr + i] for i in range(1, 3 + 1))
    if prog[ptr] == 1:
        prog[progCode[2]] = prog[progCode[0]] + prog[progCode[1]]
    else:
        prog[progCode[2]] = prog[progCode[0]] * prog[progCode[1]]
    ptr += 4
print(prog[0])

# part 2
target = 19690720
foundRes = None
for noun in range(100):
    for verb in range(100):
        prog[:] = list(util.getInts(inp))
        prog[1] = noun
        prog[2] = verb
        ptr = 0
        while prog[ptr] != 99:
            assert prog[ptr] in (1, 2)
            progCode = tuple(prog[ptr + i] for i in range(1, 3 + 1))
            if prog[ptr] == 1:
                prog[progCode[2]] = prog[progCode[0]] + prog[progCode[1]]
            else:
                prog[progCode[2]] = prog[progCode[0]] * prog[progCode[1]]
            ptr += 4
        if prog[0] == target:
            foundRes = (noun, verb)
            break
    if foundRes is not None:
        break
assert foundRes is not None
print(100 * foundRes[0] + foundRes[1])

