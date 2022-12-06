import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=6, y=2022)
l = len(inp)

# part 1
print(util.firstSuchThat(range(l - 4), lambda i: len(set(inp[i:i + 4])) == 4)[0] + 4)

# part 2
print(util.firstSuchThat(range(l - 14), lambda i: len(set(inp[i:i + 14])) == 14)[0] + 14)
