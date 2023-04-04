import AOCInit
import util
import re
from functools import cache

if __name__ != '__main__':
    exit()

inp = util.getInput(d=19, y=2020)

(ruleSpec, msgLines) = inp.split('\n\n')
rules = {
    line.split(': ')[0]: \
            tuple(pr.split() for pr in line.split(': ')[1].strip('"').split(' | '))
    for line in ruleSpec.splitlines()
}
msgs = msgLines.splitlines()

# part 1
# Why does this work?
# The generated pattern is ~11k char long but only takes ~300ms for this part
genedRegexStr: dict[str, str] = dict()
def getRegexStr(ruleIdx: str) -> str:
    if ruleIdx not in genedRegexStr:
        genedRegexStr[ruleIdx] = (
                ruleIdx
                if ruleIdx not in rules
                else '|'.join(frozenset(''.join('(?:' + getRegexStr(p) + ')'
                                                for p in gp)
                              for gp in rules[ruleIdx])))
    return genedRegexStr[ruleIdx]

rule0 = re.compile('^' + getRegexStr('0') + '$')
print(util.count(msgs, lambda line: rule0.match(line) is not None))

# part 2
# ~200ms
rules['8'] = (['42'], ['42', '8']) # 42+
rules['11'] = (['42', '31'], ['42', '11', '31']) # 42{n}31{n}, not regular
@cache
def getMinMatchLen(ruleIdx: str) -> int:
    if ruleIdx not in rules:
        return len(ruleIdx) # 1?
    return min(sum(getMinMatchLen(atom) for atom in gp)
               for gp in rules[ruleIdx])

eachRepMinLen = getMinMatchLen('42') + getMinMatchLen('31')
maxRepCount = (max(map(len, msgs)) + eachRepMinLen - 1) // eachRepMinLen
genedRegexStr.clear()
def getRegexStrAgain(ruleIdx: str) -> str:
    if ruleIdx not in genedRegexStr:
        if ruleIdx not in rules:
            genedRegexStr[ruleIdx] = ruleIdx
        elif ruleIdx == '8':
            genedRegexStr['8'] = '(?:' + getRegexStrAgain('42') + ')+'
        elif ruleIdx == '11':
            rule42 = '(?:' + getRegexStrAgain('42') + ')'
            rule31 = '(?:' + getRegexStrAgain('31') + ')'
            genedRegexStr['11'] = '|'.join('(?:' + rule42 + f'{{{i}}}' + rule31 + f'{{{i}}}' + ')'
                                           for i in range(1, maxRepCount + 1))
        else:
            genedRegexStr[ruleIdx] = '|'.join(
                    frozenset(''.join('(?:' + getRegexStrAgain(p) + ')'
                                      for p in gp)
                              for gp in rules[ruleIdx]))
    return genedRegexStr[ruleIdx]

rule0 = re.compile('^' + getRegexStrAgain('0') + '$')
print(util.count(msgs, lambda line: rule0.match(line) is not None))


