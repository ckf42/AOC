import argparse
import pathlib
from shutil import copy

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('day',
                        type=int,
                        help="The day of the challenge")
    parser.add_argument('--force', '-f',
                        action='store_true',
                        help="Overwrite if solution file already exists")
    return parser.parse_args()

def main():
    args = getArgs()
    assert 1 <= args.day < 26, f"Invalid day: {args.day}"
    cwd = pathlib.Path.cwd()
    assert cwd.stem.isnumeric(), f"Cannot parse year from CWD: {cwd.stem}"
    year = cwd.stem
    solTempLoc = (cwd / '../solTemp.py').resolve()
    assert solTempLoc.is_file(), "Cannot find the solution template"
    outputFilePath = cwd / f'day{args.day}.py'
    if not args.force:
        assert not outputFilePath.is_file(), f"{outputFilePath.name} already exists"
    copy(solTempLoc, outputFilePath)
    fileContent = list()
    with outputFilePath.open(mode='r') as f:
        fileContent = f.readlines()
    with outputFilePath.open(mode='w') as f:
        for line in fileContent:
            print(line.rstrip().replace('{{day}}', str(args.day)).replace('{{year}}', year),
                  file=f)


if __name__ == '__main__':
    main()
