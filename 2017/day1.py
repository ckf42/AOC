import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=1, y=2017).strip()

# part 1
print(sum(int(inp[i])
          for i in range(len(inp) - 1)
          if inp[i] == inp[i + 1])
      + (int(inp[-1]) if inp[0] == inp[-1] else 0))

# part 2
l = len(inp)
print(sum(int(inp[i])
          for i in range(l)
          if inp[i] == util.cycInd(inp, i + l // 2)))

