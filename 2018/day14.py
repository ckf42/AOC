import AOCInit
import util

if __name__ != '__main__':
    exit()

# TODO: optimize. currently takes ~1s for part 1, ~30s for part 2

inp = util.getInput(d=14, y=2018)

inp = inp.strip()
recpCountToMake = int(inp)
recipeList = [3, 7]
elfPtr = [0, 1]

# part 1
while len(recipeList) < 10 + recpCountToMake:
    newRecp = sum(recipeList[ptr] for ptr in elfPtr)
    recipeList.extend(divmod(newRecp, 10) if newRecp >= 10 else (newRecp,))
    for i in range(2):
        elfPtr[i] = (elfPtr[i] + 1 + recipeList[elfPtr[i]]) % len(recipeList)
print(''.join(map(str, recipeList[recpCountToMake:recpCountToMake + 10])))


# part 2
if inp in (ss := ''.join(map(str, recipeList))):
    print(ss.index(inp))
else:
    inpDig = list(map(int, inp))
    ipl = len(inp)
    found = False
    oldLen = len(recipeList)
    while not found:
        for _ in range(100000):
            newRecp = sum(recipeList[ptr] for ptr in elfPtr)
            recipeList.extend(divmod(newRecp, 10) if newRecp >= 10 else (newRecp,))
            for i in range(2):
                elfPtr[i] = (elfPtr[i] + 1 + recipeList[elfPtr[i]]) % len(recipeList)
        try:
            print(''.join(map(str, recipeList[oldLen - ipl:])).index(inp) + oldLen - ipl)
            found = True
        except ValueError:
            oldLen = len(recipeList)


