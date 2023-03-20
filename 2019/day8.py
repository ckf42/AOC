import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=8, y=2019)
w = 25
h = 6

layers = util.splitIntoGp(inp.strip(), w * h, allowRemain=False)

# part 1
mZLayer = util.argmin(range(len(layers)), lambda l: util.countItem(layers[l], '0'))
print(util.countItem(layers[mZLayer], '1') * util.countItem(layers[mZLayer], '2'))

# part 2
for j in range(h):
    for i in range(w):
        print(util.consoleChar(
            layer[i + w * j] == '1'
            if (layer := util.firstSuchThat(layers,
                                            lambda l: l[i + w * j] != '2')[1]) is not None
            else None),
              end='')
    print('')
print('')

