import AOCInit
import util
from functools import cmp_to_key
from collections import Counter

if __name__ != '__main__':
    exit()

inp = util.getInput(d=7, y=2023)
hands = tuple(
        (line.split()[0], int(line.split()[1]))
        for line in inp.splitlines())

def getRanks(handList: tuple[str, ...], isPart2=False):
    cardOrdering: str = 'AKQT98765432J' if isPart2 else 'AKQJT98765432'  # small = strong
    jRk: int = cardOrdering.index('J')
    handOrdList: tuple[tuple[int, ...], ...] = tuple(
            tuple(cardOrdering.index(c) for c in h)
            for h in handList)

    def getType(hand: tuple[int, ...]) -> int:
        c: Counter[int] = Counter(hand)
        if isPart2 and jRk in c and len(c) != 1:
            cardCountOrder: list[int] = sorted(
                    tuple(c.keys()),
                    key=lambda k: c[k],
                    reverse=True)
            target: int | None = util.firstSuchThat(
                    cardCountOrder,
                    lambda card: card != jRk)[1]
            assert target is not None
            c[target] += c[jRk]
            del c[jRk]
        m = max(c.values())
        return 10 * len(c) + 5 - m

    def handCmp(h1: tuple[int, ...], h2: tuple[int, ...]) -> int:
        # is hand1 stronger?
        t1, t2 = getType(h1), getType(h2)
        if t1 == t2:
            return 1 if h1 <= h2 else -1
        return 1 if t1 <= t2 else -1

    return sorted(util.rangeLen(handOrdList),
                  key=cmp_to_key(lambda i, j: handCmp(handOrdList[i], handOrdList[j])))

# part 1
print(sum((i + 1) * hands[r][1]
          for i, r in enumerate(getRanks(tuple(h[0] for h in hands), isPart2=False))))

# part 2
print(sum((i + 1) * hands[r][1]
          for i, r in enumerate(getRanks(tuple(h[0] for h in hands), isPart2=True))))

