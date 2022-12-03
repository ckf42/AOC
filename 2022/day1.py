import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=1, y=2022)
arr = list(sum(int(c) for c in elf.split()) for elf in inp.split('\n\n'))

# part 1
print(max(arr))

# part 2
arr.sort(reverse=True)
print(sum(arr[:3]))
