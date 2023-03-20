import AOCInit
import util
from itertools import permutations as perm
import typing as tp
from collections import deque

if __name__ != '__main__':
    exit()

inp = util.getInput(d=7, y=2019)

code = util.getInts(inp)

argCountDict: dict[int, int] = {
    1: 3, 2: 3,
    3: 1, 4: 1,
    5: 2, 6: 2,
    7: 3, 8: 3,
}

def intCodeProg(sourceCode: tp.Sequence[int],
                inputValues: tp.Iterable[int]) -> tp.Generator[int, int, None]:
    prog: list[int] = list(sourceCode)
    inputBuffer: deque[int] = deque(inputValues)
    outputBuffer: deque[int] = deque()

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
        modes = tuple(map(int,
                          str(prog[ptr] // 100).zfill(argCount)[::-1]))
        if thisOpCode == 1:
            prog[paras[2]] = access(paras[0], modes[0]) + access(paras[1], modes[1])
        elif thisOpCode == 2:
            prog[paras[2]] = access(paras[0], modes[0]) * access(paras[1], modes[1])
        elif thisOpCode == 3:
            prog[paras[0]] = (inputBuffer.popleft()
                              if len(inputBuffer) != 0
                              else (yield outputBuffer.popleft()))
        elif thisOpCode == 4:
            outputBuffer.append(access(paras[0], modes[0]))
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
    for val in outputBuffer:
        yield val

# part 1
maxSig = None
for p in perm(range(5), 5):
    lastOut = 0
    for i in range(5):
        lastOut = next(intCodeProg(code, (p[i], lastOut)))
    if maxSig is None or maxSig < lastOut:
        maxSig = lastOut
print(maxSig)


# part 2
maxSig = None
for p in perm(range(5, 10), 5):
    ampList: list[tp.Generator[int, int, None]] = list()
    ampPtr = 0
    lastOut = 0
    lastFromE = None
    while True:
        if ampPtr >= len(ampList):
            ampList.append(intCodeProg(code, (p[ampPtr], lastOut)))
            lastOut = next(ampList[ampPtr])
        else:
            try:
                lastOut = ampList[ampPtr].send(lastOut)
            except StopIteration:
                break
        if ampPtr % 5 == 4:
            lastFromE = lastOut
        ampPtr = (ampPtr + 1) % 5
    if lastFromE is not None and (maxSig is None or maxSig < lastFromE):
        maxSig = lastFromE
print(maxSig)

