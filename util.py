import typing as _typing
import collections.abc as _abc
import pathlib as _pathlib
import requests as _rq
import re as _re

# exposed in envir
import functools as ft
import itertools as it

if __name__ == '__main__':
    exit()

_T = _typing.TypeVar('T')

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

def firstSuchThat(arr: _typing.Iterable[_T],
                  cond: _typing.Callable[_T, bool]) -> _typing.Optional[_T]:
    return next(filter(cond, arr), None)

def cycInd(arr: _abc.Sequence[_T], index: int) -> _T:
    return arr[index % len(arr)]

def prod(arr: _typing.Iterable[float]) -> float:
    return ft.reduce(lambda x, y: x * y, arr)

def takeExcept(arr: _abc.Sequence[_T], index: int) -> _abc.Sequence[_T]:
    return arr[:index] + arr[index + 1:]

def splitAt(arr: _abc.Sequence[_T], index: int) -> tuple[_abc.Sequence[_T]]:
    return (arr[:index], arr[index:])

def getInts(s: str) -> tuple[int]:
    return tuple(map(int, _re.findall(r'\d+', s)))

def splitIntoGp(arr: _abc.Sequence[_T], gpSize: int) ->tuple[tuple[_T]]:
    return tuple(tuple(arr[ind + i]
                       for i in range(gpSize))
                 for ind in range(0, len(arr), gpSize))

