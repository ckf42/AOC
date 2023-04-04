import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=8, y=2020)
instruction = {
    i: (line.split()[0], int(line.split()[1]))
    for i, line in enumerate(inp.splitlines())
}

# part 1
executedInst: set[int] = set()
accum = 0
instPtr = 0
while True:
    if instPtr in executedInst:
        break
    executedInst.add(instPtr)
    ptrInc = 1
    (inst, arg) = instruction[instPtr]
    if inst == 'acc':
        accum += arg
    elif inst =='jmp':
        ptrInc = arg
    elif inst == 'nop':
        pass
    else:
        raise RuntimeError(f"Unknown instruction: {inst}")
    instPtr += ptrInc
print(accum)

# part 2
relevantInst = set(filter(lambda idx: instruction[idx][0] in ('nop', 'jmp'),
                          executedInst))
for changedIdx in relevantInst:
    executedInst.clear()
    accum = 0
    instPtr = 0
    instFound = False
    while True:
        if instPtr in executedInst:
            break
        if instPtr not in instruction:
            print(accum)
            instFound = True
            break
        executedInst.add(instPtr)
        ptrInc = 1
        (inst, arg) = instruction[instPtr]
        if instPtr == changedIdx:
            inst = 'nop' if inst == 'jmp' else 'jmp'
        if inst == 'acc':
            accum += arg
        elif inst =='jmp':
            ptrInc = arg
        elif inst == 'nop':
            pass
        else:
            raise RuntimeError(f"Unknown instruction: {inst}")
        instPtr += ptrInc
    if instFound:
        break


