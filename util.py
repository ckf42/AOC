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

def lastSuchThat(arr: _tp.Iterable[_T],
                 cond: _tp.Callable[_T, bool]) -> tuple[_tp.Optional[int], _tp.Optional[_T]]:
    lastTrue = (None, None)
    filterObj = filter(lambda t: cond(t[1]), enumerate(arr))
    while (o := next(filterObj, None)) is not None:
        lastTrue = o
    return lastTrue

def firstAccumSuchThat(
        arr: _tp.Iterable[_T],
        func: _tp.Callable[[_T, _T], _T],
        cond: _tp.Callable[_T, bool]
        ) -> tuple[_tp.Optional[int], _tp.Optional[_T], _tp.Optional[_T]]:
    return next(filter(lambda t: cond(t[2]),
                       zip(_it.count(0), arr, _it.accumulate(arr, func))),
                (None, None, None))

def lastAccumSuchThat(
        arr: _tp.Iterable[_T],
        func: _tp.Callable[[_T, _T], _T],
        cond: _tp.Callable[_T, bool]
        ) -> tuple[_tp.Optional[int], _tp.Optional[_T], _tp.Optional[_T]]:
    lastTrue = (None, None, None)
    filterObj = filter(lambda t: cond(t[2]),
                       zip(_it.count(0), arr, _it.accumulate(arr, func)))
    while (o := next(filterObj, None)) is not None:
        lastTrue = o
    return lastTrue

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

def splitIntoGp(arr: _abc.Sequence[_T],
                gpSize: int,
                allowRemain: bool = True) ->tuple[tuple[_T]]:
    lArr = len(arr)
    return tuple(tuple(arr[gpInit:(min(gpInit + gpSize, lArr)
                                   if allowRemain
                                   else gpInit + gpSize)])
                 for gpInit in range(0, lArr, gpSize))

def takeFromEvery(arr: _abc.Sequence[_T],
                  gpSize: int,
                  idx: int = 0,
                  takeFromRemain: bool = True) -> tuple[_T]:
    lArr = len(arr)
    return tuple(arr[gpInit + idx]
                 for gpInit in range(0, lArr, gpSize)
                 if takeFromRemain or gpInit + gpSize <= lArr)

def sub(originalSym: _abc.Collection[_T],
        targetSym: _abc.Collection[_S],
        arr: _abc.Collection[_T],
        discard: bool = False) -> tuple[_tp.Union[_T, _S]]:
    replacementDict = {k: v for k, v in zip(originalSym, targetSym)}
    return tuple(replacementDict.get(c, c)
                 for c in arr
                 if not discard or c in replacementDict)

def subChar(originalSym: str, targetSym: str, s: str) -> str:
    return s.translate(str.maketrans(originalSym, targetSym))

