import typing as _typing
import pathlib as _pathlib
import requests as _rq

if __name__ == '__main__':
    exit()

_T = _typing.TypeVar('T')

def getInput(d: _typing.Optional[int] = None,
             y: int = 2022,
             force: bool = False) -> str:
    if force or not _pathlib.Path('input').is_file():
        with open('session', 'rt') as sessKey:
                  r = _rq.get(f'https://adventofcode.com/{y}/day/{d}/input',
                             cookies={'session': sessKey.read().strip()}).text
        with open(f'input{d}', 'wt') as f:
            print(r, file=f, end='')
        return r
    else:
        with open(f'input{d}', 'rt') as f:
            return f.read()

def firstEleSuchThat(items: _typing.Iterable[_T],
                     cond: _typing.Callable[_T, bool]) -> _typing.Optional[_T]:
    for i in items:
        if cond(i):
            return i
    return None

