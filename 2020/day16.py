import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=16, y=2020)

(ruleSpec, ownTicketSpec, nearbyTicketSpec) = inp.split('\n\n')
fieldRanges = {
    line.split(': ', maxsplit=1)[0]: \
        util.IntegerIntervals(
            *util.splitIntoGp(util.getInts(line, allowNegative=False),
                              2, allowRemain=False))
    for line in ruleSpec.splitlines()
}
totalRange = util.IntegerIntervals.fromUnioning(*fieldRanges.values())
ticketLists = (util.getInts(ownTicketSpec.splitlines()[1]),) \
        + tuple(util.getInts(line) for line in nearbyTicketSpec.splitlines()[1:])

# part 1
errorRate = 0
validTickets = set(range(len(ticketLists)))
for idx, ticket in enumerate(ticketLists[1:]):
    for field in ticket:
        if field not in totalRange:
            errorRate += field
            validTickets.discard(idx + 1)
print(errorRate)

# part 2
fieldVals = util.takeApart(tuple(ticketLists[idx] for idx in validTickets))
possibleFieldNames: tuple[set[str], ...] = tuple(
    set(filter(lambda fname: all(val in fieldRanges[fname] for val in valList),
               fieldRanges.keys()))
    for valList in fieldVals
)
idxToField = [None for _ in range(len(fieldVals))]
while (uniqIdx := util.firstIdxSuchThat(possibleFieldNames,
                                        lambda pfn: len(pfn) == 1)) is not None:
    fn = possibleFieldNames[uniqIdx].pop()
    idxToField[uniqIdx] = fn
    for s in possibleFieldNames:
        s.discard(fn)
assert all(fn is not None for fn in idxToField)
departure = tuple(ticketLists[0][i]
                  for i, fn in enumerate(idxToField)
                  if fn.startswith('departure'))
assert len(departure) == 6
print(util.prod(departure))

