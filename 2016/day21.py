import AOCInit
import util
from collections import deque

if __name__ != '__main__':
    exit()

inp = """\
swap position 4 with position 0
swap letter d with letter b
reverse positions 0 through 4
rotate left 1 step
move position 1 to position 4
move position 3 to position 0
rotate based on position of letter b
rotate based on position of letter d\
"""
buffer = deque('abcde')
inp = util.getInput(d=21, y=2016)
buffer = deque('abcdefgh')

instructions = tuple(l.split() for l in inp.splitlines())

# part 1
for inst in instructions:
    if inst[0] == 'swap':
        idx = tuple((int if inst[1] == 'position' else buffer.index)(inst[i])
                    for i in (2, 5))
        buffer[idx[0]], buffer[idx[1]] = buffer[idx[1]], buffer[idx[0]]
    elif inst[0] == 'rotate':
        offset = 0
        if inst[1] == 'based':
            offset = buffer.index(inst[6])
            offset += 1 if offset < 4 else 2
        else:
            offset = int(inst[2]) * (-1 if inst[1] == 'left' else 1)
        buffer.rotate(offset)
    elif inst[0] == 'reverse':
        (s, e) = (int(inst[2]), int(inst[4]))
        for i in range((e - s + 1) // 2):
            buffer[s + i], buffer[e - i] = buffer[e - i], buffer[s + i]
    else:
        # move
        buffer.rotate(-int(inst[2]) - 1)
        c = buffer.pop()
        buffer.rotate(int(inst[2]))
        buffer.insert(int(inst[5]), c)
    # print(inst)
    # print(''.join(buffer))
print(''.join(buffer))

# part 2
buffer = deque('fbgdceah')
rotBImage = tuple((i, (2 * i + (1 if i < 4 else 2)) % len(buffer))
                  for i in range(len(buffer)))
rotBOffsetByImage = dict()
for i, im in rotBImage:
    if im not in rotBOffsetByImage:
        rotBOffsetByImage[im] = list()
    rotBOffsetByImage[im].append(i + (1 if i < 4 else 2))
buffList = [buffer]
for inst in instructions[::-1]:
    if inst[0] == 'swap':
        for bidx in range(len(buffList)):
            idx = tuple((int if inst[1] == 'position' else buffList[bidx].index)(inst[i])
                        for i in (2, 5))
            buffList[bidx][idx[0]], buffList[bidx][idx[1]] = buffList[bidx][idx[1]], buffList[bidx][idx[0]]
    elif inst[0] == 'rotate':
        if inst[1] == 'based':
            newBuff = set()
            for bidx in range(len(buffList)):
                im = buffList[bidx].index(inst[6])
                for offset in rotBOffsetByImage[im]:
                    buffList[bidx].rotate(-offset)
                    newBuff.add(tuple(buffList[bidx]))
                    buffList[bidx].rotate(offset)
            buffList[:] = list(deque(t) for t in newBuff)
        else:
            offset = int(inst[2]) * (-1 if inst[1] == 'left' else 1)
            for bidx in range(len(buffList)):
                buffList[bidx].rotate(-offset)
    elif inst[0] == 'reverse':
        (s, e) = (int(inst[2]), int(inst[4]))
        for i in range((e - s + 1) // 2):
            for bidx in range(len(buffList)):
                buffList[bidx][s + i], buffList[bidx][e - i] = buffList[bidx][e - i], buffList[bidx][s + i]
    else:
        # move
        for bidx in range(len(buffList)):
            buffList[bidx].rotate(-int(inst[5]) - 1)
            c = buffList[bidx].pop()
            buffList[bidx].rotate(int(inst[5]))
            buffList[bidx].insert(int(inst[2]), c)
    # print(inst)
    # print(tuple(''.join(b) for b in buffList))
print(tuple(''.join(b) for b in buffList))

