from pathlib import Path
import urllib.request as ulq
import urllib.error as ule
import re

STATPAGE_URL = "https://adventofcode.com/2015/events"
STAR_REGEX = re.compile(
    r'<a href="/\d*">\[(\d+)\]</a> *<span class="star-count">(\d+)\*</span> *<span class="quiet">/ (\d+)\*'
)
TABLE_START = "<!-- progress table start -->"
TABLE_END = "<!-- progress table end -->"

BASE_PATH = Path(__file__).parent


def getStarCounts() -> dict[int, tuple[int, int]]:
    rt: str | None = None
    with (BASE_PATH / "session").open("rt") as sessKey:
        try:
            sKey = sessKey.read().strip()
            with ulq.urlopen(
                ulq.Request(STATPAGE_URL, headers={"Cookie": f"session={sKey}", "User-Agent": "github.com/ckf42/AOC"})
            ) as resp:
                rt = resp.fp.read().decode()
        except ule.HTTPError as e:
            detail = e.fp.read().decode()
            raise RuntimeError(f"Failed to fetch status page: {e.reason}\nDetail: {detail}") from e
    assert rt is not None, "Failed to fetch status page"
    resDict: dict[int, tuple[int, int]] = {
        int(items[0]): (int(items[1]), int(items[2])) for items in STAR_REGEX.findall(rt)
    }
    assert len(resDict) != 0, "Cannot find star count. Please ensure you have logged in."
    return resDict


def main() -> None:
    with (BASE_PATH / "README.md").open("rt") as f:
        readmeLines = f.read().splitlines()
    assert readmeLines is not None, "Failed to read readme file"
    startIdx = readmeLines.index(TABLE_START)
    endIdx = readmeLines.index(TABLE_END)
    starDict: dict[int, tuple[int, int]] = getStarCounts()
    tableLines: list[str] = ["| Year | Star Count |", "| ---- | ---------- |"]
    for year in sorted(starDict.keys()):
        print(f"{year}: {starDict[year][0]} / {starDict[year][1]}")
        tableLines.append(f"| {str(year).center(4)} | {f'{starDict[year][0]} / {starDict[year][1]}'.center(10)} |")
    readmeLines[startIdx + 1 : endIdx] = tableLines

    with (BASE_PATH / "README.md").open("wt") as f:
        for line in readmeLines:
            print(line, file=f)


if __name__ == "__main__":
    main()
