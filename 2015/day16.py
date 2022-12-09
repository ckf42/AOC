import AOCInit
import util

if __name__ != '__main__':
    exit()

aunts = tuple((ls[0], {itemPair[0]: int(itemPair[1])
                       for item in ls[1].split(', ')
                       if (itemPair := item.split(': '))})
              for l in util.getInput(d=16, y=2015).splitlines()
              if (ls := l.split(': ', maxsplit=1)))

knownInfo = """children: 3
cats: 7
samoyeds: 2
pomeranians: 3
akitas: 0
vizslas: 0
goldfish: 5
trees: 3
cars: 2
perfumes: 1"""
knownInfo = {ls[0]: int(ls[1]) for l in knownInfo.splitlines() if (ls := l.split(': '))}

# part 1
print(util.firstSuchThat(aunts,
                         lambda sue: all(knownInfo[prop] == val
                                         for prop, val in sue[1].items()))[1][0])

# part 2
def compare(prop, val):
    if prop in ('cats', 'trees'):
        return val > knownInfo[prop]
    elif prop in ('pomeranians', 'goldfish'):
        return val < knownInfo[prop]
    else:
        return val == knownInfo[prop]

print(util.firstSuchThat(aunts,
                         lambda sue: all(compare(prop, val)
                                         for prop, val in sue[1].items()))[1][0])

