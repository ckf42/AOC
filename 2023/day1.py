import AOCInit
import util  # yes, I forgot how to use my own library. How do you know?

if __name__ != '__main__':
    exit()

inp = util.getInput(d=1, y=2023).splitlines()

# part 1
nums = list(list(int(c) for c in line if c.isdigit())
            for line in inp)
print(sum(np[0] * 10 + np[-1] for np in nums))

# part 2
letters = ('one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine')
nums = list()
for line in inp:
    lineNum = list()
    for i in util.rangeLen(line):
        if line[i].isdigit():
            lineNum.append(int(line[i]))
        else:
            for idx, w in enumerate(letters):
                if line[i:].startswith(w):
                    lineNum.append(idx + 1)
    nums.append(lineNum)
print(sum(np[0] * 10 + np[-1] for np in nums))

