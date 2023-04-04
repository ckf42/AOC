import AOCInit
import util
import re

if __name__ != '__main__':
    exit()

inp = util.getInput(d=4, y=2020)

# part 1
batch = tuple(
        {
            pr[0]: pr[1]
            for kv in part.split()
            if (pr := kv.split(':')) is not None
        }
        for part in inp.split('\n\n')
)
requiredField = ('byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid')
print(util.count(batch, lambda p: all(n in p for n in requiredField)))

# part 2
byrRange = range(1920, 2002 + 1)
iyrRange = range(2010, 2020 + 1)
eyrRange = range(2020, 2030 + 1)

def isValidHgt(hgt: str):
    if hgt.endswith('cm'):
        return int(hgt[:-2]) in range(150, 193 + 1)
    elif hgt.endswith('in'):
        return int(hgt[:-2]) in range(59, 76 + 1)
    else:
        return False

eclAllowList = frozenset(('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'))
hclRegex = re.compile('^#[0-9a-f]{6}$')
pidRegex = re.compile('^[0-9]{9}$')
def isValid(p):
    return int(p.get('byr', '0')) in byrRange \
            and int(p.get('iyr', '0')) in iyrRange \
            and int(p.get('eyr', '0')) in eyrRange \
            and isValidHgt(p.get('hgt', '')) \
            and hclRegex.search(p.get('hcl', '')) is not None \
            and p.get('ecl', '') in eclAllowList \
            and pidRegex.search(p.get('pid', '')) is not None

print(util.count(batch, isValid))

