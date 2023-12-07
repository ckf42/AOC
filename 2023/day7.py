import AOCInit
import util
from collections import Counter

if __name__ != '__main__':
    exit()

inp = util.getInput(d=7, y=2023)
hands, handPts = util.transpose(tuple(
        (line.split()[0], int(line.split()[1]))
        for line in inp.splitlines()))

def rankedOrdering(handList: tuple[str, ...], isPart2=False) -> list[int]:
    cardOrder: str = 'AKQT98765432J' if isPart2 else 'AKQJT98765432'  # small = strong

    def getType(hand: str) -> int:
        c: Counter[str] = Counter(hand)
        if isPart2 and len(c) != 1 and 'J' in c:
            target: str | None = util.firstSuchThat(
                    (pr[0] for pr in c.most_common()),
                    lambda card: card != 'J')[1]
            assert target is not None
            c[target] += c['J']
            del c['J']
        m = max(c.values())
        return 10 * len(c) + 5 - m

    rankedIndices = sorted(
            util.rangeLen(handList),
            key=lambda hidx: tuple(cardOrder.index(c) for c in handList[hidx]),
            reverse=True)
    rankedIndices.sort(key=lambda hidx: getType(handList[hidx]), reverse=True)
    return rankedIndices


# part 1
print(sum((rk + 1) * handPts[hidx]
          for rk, hidx in enumerate(
              rankedOrdering(hands, isPart2=False))))

# part 2
print(sum((rk + 1) * handPts[hidx]
          for rk, hidx in enumerate(
              rankedOrdering(hands, isPart2=True))))

