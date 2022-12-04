import typing as _tp
import collections.abc as _abc
import pathlib as _pathlib
import requests as _rq
import re as _re
import functools as _ft
import itertools as _it

if __name__ == '__main__':
    exit()

_T = _tp.TypeVar('T')
_S = _tp.TypeVar('S')

def getInput(d: int,
             y: int,
             force: bool = False) -> str:
    if force or not _pathlib.Path('input').is_file():
        with open('../session', 'rt') as sessKey:
            r = _rq.get(f'https://adventofcode.com/{y}/day/{d}/input',
                        cookies={'session': sessKey.read().strip()}).text
        with open(f'input{d}', 'wt') as f:
            print(r, file=f, end='')
        return r
    else:
        with open(f'input{d}', 'rt') as f:
            return f.read()

def firstSuchThat(arr: _tp.Iterable[_T],
                  cond: _tp.Callable[_T, bool]) -> tuple[_tp.Optional[int], _tp.Optional[_T]]:
    return next(filter(lambda t: cond(t[1]), enumerate(arr)), (None, None))

def firstAccumSuchThat(
        arr: _tp.Iterable[_T],
        func: _tp.Callable[[_T, _T], _T],
        cond: _tp.Callable[_T, bool]
        ) -> tuple[_tp.Optional[int], _tp.Optional[_T], _tp.Optional[_T]]:
    return next(filter(lambda t: cond(t[2]),
                       zip(_it.count(0), arr, _it.accumulate(arr, func))),
                (None, None, None))

def cycInd(arr: _abc.Sequence[_T], index: int) -> _T:
    return arr[index % len(arr)]

def prod(arr: _tp.Iterable[float]) -> float:
    return _ft.reduce(lambda x, y: x * y, arr)

def takeExcept(arr: _abc.Sequence[_T], index: int) -> _abc.Sequence[_T]:
    return arr[:index] + arr[index + 1:]

def splitAt(arr: _abc.Sequence[_T],
            index: int) -> tuple[_abc.Sequence[_T], _abc.Sequence[_T]]:
    return (arr[:index], arr[index:])

def getInts(s: str) -> tuple[int]:
    return tuple(map(int, _re.findall(r'\d+', s)))

def splitIntoGp(arr: _abc.Sequence[_T], gpSize: int) ->tuple[tuple[_T]]:
    return tuple(tuple(arr[ind + i] for i in range(gpSize))
                 for ind in range(0, len(arr), gpSize))

def sub(originalSym: _abc.Collection[_T],
        targetSym: _abc.Collection[_S],
        arr: _abc.Collection[_T],
        discard: bool = False) -> tuple[_tp.Union[_T, _S]]:
    replacementDict = {k: v for k, v in zip(originalSym, targetSym)}
    return tuple(replacementDict.get(c, c) for c in arr if not discard or c in replacementDict)

def subChar(originalSym: str, targetSym: str, s: str) -> str:
    return s.translate(str.maketrans(originalSym, targetSym))

