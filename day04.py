import typing
import re
import math


def day04_part1(file_name: str) -> int:
    # open the input file
    f: typing.TextIO = open(file_name, "r")

    # read the input file, line by line
    result: int = 0
    input: list = []
    for line in f:
        parsed_line: list = re.match(r"^Card\s+(\d+): (.*)\|(.*)$", line)
        winners: list = re.findall(r"\d+", parsed_line.groups()[1])
        all: list = re.findall(r"\d+", parsed_line.groups()[2])

        # find all elements of "winners" who are also present in "all"
        # and return the length of the resulting list
        won: int = len([x for x in winners if x in all])

        # if won is at least 1, add 2 to the power of ("won"-1) to the result
        if won > 0:
            result += int(math.pow(2, won-1))

    return result


def test_day04_part1a():
    assert day04_part1("./input/day04a.txt") == 13


def test_day04_part1b():
    assert day04_part1("./input/day04b.txt") == 26218

