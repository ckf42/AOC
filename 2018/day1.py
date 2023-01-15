import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=1, y=2018)

freqDelta = util.getInts(inp)

# part 1
print(sum(freqDelta))

# part 2
seenFreq = {0}
currFreq = 0
seenRepeat = False
while not seenRepeat:
    for freq in freqDelta:
        currFreq += freq
        if currFreq in seenFreq:
            print(currFreq)
            seenRepeat = True
            break
        seenFreq.add(currFreq)

