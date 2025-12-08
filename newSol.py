import argparse
import datetime
import pathlib

BASE_PATH = pathlib.Path(__file__).parent


def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("day", nargs="?", type=int, help="The day of the challenge")
    parser.add_argument("--force", "-f", action="store_true", help="Overwrite if solution file already exists")
    args = parser.parse_args()
    if args.day is None:
        today = datetime.date.today()
        if today.month == 12 and today.day < 26:
            args.day = today.day
        else:
            parser.error("day not given. Cannot deduce from date")
    return args


def main():
    args = getArgs()
    day: int = args.day
    assert 1 <= day < 26, f"Invalid day: {day}"
    cwd = pathlib.Path.cwd()
    year = cwd.stem
    assert year.isnumeric(), f"Cannot parse year from cwd: {year}"
    solTempLoc = (BASE_PATH / "solTemp.py").resolve()
    assert solTempLoc.is_file(), "Cannot find the solution template"
    outputFilePath = BASE_PATH / str(year) / f"day{day}.py"
    if not args.force:
        assert not outputFilePath.is_file(), f"{outputFilePath.name} already exists"
    fileContent = list()
    with solTempLoc.open(mode="r") as f:
        fileContent = f.readlines()
    if day == 25 or (int(year) >= 2025 and day == 12):
        fileContent[-2] = "# no part 2"
    with outputFilePath.open(mode="w") as f:
        for line in fileContent:
            print(line.rstrip().replace("{{day}}", str(day)).replace("{{year}}", year), file=f)


if __name__ == "__main__":
    main()
