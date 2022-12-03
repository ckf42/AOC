import AOCInit
import util
import re

inp = util.getInput(d=5, y=2015).splitlines()

# part 1
regexTrue = [
    re.compile(r'[aeiou].*[aeiou].*[aeiou]', re.I),
    re.compile(r'(.)\1', re.I),
]
withoutSubStr = ['ab', 'cd', 'pq', 'xy']
print(sum(all(r.search(s) for r in regexTrue) and all(ss not in s for ss in withoutSubStr)
          for s in inp))

# part 2
regexTrue = [
    re.compile(r'(..).*\1', re.I),
    re.compile(r'(.).\1', re.I)
]
print(sum(all(r.search(s) for r in regexTrue) for s in inp))
