import typing
import pathlib
import requests as rq

if __name__ == '__main__':
    exit()


def getInput(d: typing.Optional[int] = None,
             y: int = 2022,
             force: bool = False) -> str:
    if force or not pathlib.Path('input').is_file():
        with open('session', 'rt') as sessKey:
                  r = rq.get(f'https://adventofcode.com/{y}/day/{d}/input',
                             cookies={'session': sessKey.read()}).text
        with open('input', 'wt') as f:
            print(r, file=f, end='')
        return r
    else:
        with open('input', 'rt') as f:
            return f.read()



