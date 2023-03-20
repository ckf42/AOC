import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=5, y=2019)

argCountDict: dict[int, int] = {
    1: 3, 2: 3,
    3: 1, 4: 1,
    5: 2, 6: 2,
    7: 3, 8: 3,
}

def exeIntCode(sourceCode: str, inputStack: list[int]) -> list[int]:
    prog: list[int] = list(util.getInts(sourceCode))
    outputStack: list[int] = list()

    def access(arg: int, mode: int) -> int:
        assert mode in (0, 1)
        if mode == 0:
            return prog[arg]
        elif mode == 1:
            return arg

    ptr = 0
    while True:
        thisOpCode = prog[ptr] % 100
        if thisOpCode == 99:
            break
        assert thisOpCode in argCountDict
        argCount = argCountDict[thisOpCode]
        newPtr = ptr + argCount + 1
        paras = prog[ptr + 1: ptr + argCount + 1]
        modes = tuple(map(int, str(prog[ptr] // 100).zfill(argCount)[::-1]))
        if thisOpCode == 1:
            prog[paras[2]] = access(paras[0], modes[0]) + access(paras[1], modes[1])
        elif thisOpCode == 2:
            prog[paras[2]] = access(paras[0], modes[0]) * access(paras[1], modes[1])
        elif thisOpCode == 3:
            prog[paras[0]] = inputStack.pop()
        elif thisOpCode == 4:
            outputStack.append(access(paras[0], modes[0]))
        elif thisOpCode == 5:
            if access(paras[0], modes[0]) != 0:
                newPtr = access(paras[1], modes[1])
        elif thisOpCode == 6:
            if access(paras[0], modes[0]) == 0:
                newPtr = access(paras[1], modes[1])
        elif thisOpCode == 7:
            prog[paras[2]] = (1
                              if access(paras[0], modes[0]) < access(paras[1], modes[1])
                              else 0)
        elif thisOpCode == 8:
            prog[paras[2]] = (1
                              if access(paras[0], modes[0]) == access(paras[1], modes[1])
                              else 0)
        ptr = newPtr
    return outputStack

# part 1
print(exeIntCode(inp, [1])[-1])

# part 2
print(exeIntCode(inp, [5])[0])

