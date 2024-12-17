import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=17, y=2024)

initReg = util.getInts(inp.split('\n\n')[0])

prog = util.getInts(inp.split('\n\n')[1])
n = len(prog)

# part 1
def runProg(initReg):
    reg = list(initReg)
    def getComboOpVal(oper):
        assert oper != 7
        if oper <= 3:
            return oper
        return reg[oper - 4]

    ptr = 0
    output = []
    while ptr < n:
        inst = prog[ptr]
        oper = prog[ptr + 1]
        if inst == 0:
            reg[0] >>= getComboOpVal(oper)
        elif inst == 1:
            reg[1] ^= oper
        elif inst == 2:
            reg[1] = getComboOpVal(oper) & 7
        elif inst == 3:
            if reg[0] != 0:
                ptr = oper - 2
        elif inst == 4:
            reg[1] ^= reg[2]
        elif inst == 5:
            output.append(getComboOpVal(oper) & 7)
        elif inst == 6:
            reg[1] = (reg[0] >> getComboOpVal(oper))
        elif inst == 7:
            reg[2] = (reg[0] >> getComboOpVal(oper))
        ptr += 2
    return tuple(output)

print(','.join(str(x) for x in runProg(initReg)))

# part 2

# def getComboOpName(oper):
#     assert oper != 7
#     if oper <= 3:
#         return oper
#     return chr(oper - 4 + ord('A'))
#
# def getInstName(inst, oper):
#     if inst == 0:
#         return f"adv: A >> {getComboOpName(oper)} -> A"
#     elif inst == 1:
#         return f"bxl: B ^ {oper} -> B"
#     elif inst == 2:
#         return f"bst: {getComboOpName(oper)} % 8 -> B"
#     elif inst == 3:
#         return f"jnz: A != 0 => jmp {oper}"
#     elif inst == 4:
#         return "bxc: B ^ C -> B"
#     elif inst == 5:
#         return f"out: {getComboOpName(oper)} % 8 -> out"
#     elif inst == 6:
#         return f"bdv: A >> {getComboOpName(oper)} -> B"
#     elif inst == 7:
#         return f"cdv: A >> {getComboOpName(oper)} -> C"
#
# for i in range(0, n, 2):
#     print(str(i).ljust(len(str(n - 2))), getInstName(prog[i], prog[i + 1]))

# manually analyzing my input, the prog is equivalent to the following python code
# while a != 0:
#     r = a % 8
#     c = (a >> (r ^ 7))
#     print((r ^ c) & 7)
#     a >>= 3

aList = [0]
for i in range(n - 1, -1, -1):
    newAList = []
    for aPrefix in aList:
        for r in range(8):
            a = (aPrefix << 3) | r
            c = (a >> (r ^ 7))
            if ((r ^ c) & 7) == prog[i]:
                newAList.append(a)
    aList = newAList
print(min(aList))

