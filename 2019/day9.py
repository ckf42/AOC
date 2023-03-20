import AOCInit
import util
import typing as tp
from collections import deque, defaultdict

if __name__ != '__main__':
    exit()

inp = util.getInput(d=9, y=2019)

code = util.getInts(inp)

argCountDict: dict[int, int] = {
    1: 3, 2: 3,
    3: 1, 4: 1,
    5: 2, 6: 2,
    7: 3, 8: 3,
    9: 1,
}

def intCodeProg(sourceCode: tp.Sequence[int],
                inputValues: tp.Iterable[int]) -> tp.Generator[int, int, None]:
    prog: defaultdict[int, int] = defaultdict(int, enumerate(sourceCode))
    inputBuffer: deque[int] = deque(inputValues)
    outputBuffer: deque[int] = deque()
    relativeBase: int = 0

    def getMem(arg: int, mode: str) -> int:
        if mode == '1':
            # immediate mode
            return arg
        else:
            return prog[getLoc(arg, mode)]

    def getLoc(arg: int, mode: str) -> int:
        assert mode != '1', "Getting location with immediate mode"
        locIdx = None
        if mode == '0':
            # positiion mode
            locIdx = arg
        elif mode == '2':
            # relative mode
            locIdx = arg + relativeBase
        if locIdx is not None:
            assert locIdx >= 0, f"Negative index: {locIdx}"
            return locIdx
        else:
            raise RuntimeError(f'Unsupported mode: {mode}')

    ptr = 0
    while True:
        thisOpCode = prog[ptr] % 100
        if thisOpCode == 99:
            break
        assert thisOpCode in argCountDict
        argCount = argCountDict[thisOpCode]
        newPtr = ptr + argCount + 1
        paras = tuple(prog[ptr + i] for i in range(1, argCount + 1))
        modes = str(prog[ptr] // 100).zfill(argCount)[::-1]
        if thisOpCode == 1:
            # sum
            prog[getLoc(paras[2], modes[2])] = \
                    getMem(paras[0], modes[0]) + getMem(paras[1], modes[1])
        elif thisOpCode == 2:
            # prod
            prog[getLoc(paras[2], modes[2])] = \
                    getMem(paras[0], modes[0]) * getMem(paras[1], modes[1])
        elif thisOpCode == 3:
            # input
            prog[getLoc(paras[0], modes[0])] = (
                    inputBuffer.popleft()
                    if len(inputBuffer) != 0
                    else (yield outputBuffer.popleft()))
        elif thisOpCode == 4:
            # output
            outputBuffer.append(getMem(paras[0], modes[0]))
        elif thisOpCode == 5:
            # jump if not zero
            if getMem(paras[0], modes[0]) != 0:
                newPtr = getMem(paras[1], modes[1])
        elif thisOpCode == 6:
            # jump if zero
            if getMem(paras[0], modes[0]) == 0:
                newPtr = getMem(paras[1], modes[1])
        elif thisOpCode == 7:
            # if is less
            prog[getLoc(paras[2], modes[2])] = (
                    1
                    if getMem(paras[0], modes[0]) < getMem(paras[1], modes[1])
                    else 0)
        elif thisOpCode == 8:
            # if is equal
            prog[getLoc(paras[2], modes[2])] = (
                    1
                    if getMem(paras[0], modes[0]) == getMem(paras[1], modes[1])
                    else 0)
        elif thisOpCode == 9:
            # change relative base
            relativeBase += getMem(paras[0], modes[0])
        else:
            raise RuntimeError(f'Unknown opcode: {thisOpCode}')
        ptr = newPtr
    for val in outputBuffer:
        yield val

# part 1
print(next(intCodeProg(code, (1,))))


# part 2
print(next(intCodeProg(code, (2,))))

