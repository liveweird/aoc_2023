import typing
import re
import math


def day04_part1(file_name: str) -> int:
    # open the input file
    f: typing.TextIO = open(file_name, "r")

    # read the input file, line by line
    result: int = 0
    for line in f:
        parsed_line: list = re.match(r"^Card\s+(\d+): (.*)\|(.*)$", line)
        winners: list = re.findall(r"\d+", parsed_line.groups()[1])
        all_numbers: list = re.findall(r"\d+", parsed_line.groups()[2])

        # find all elements of "winners" who are also present in "all"
        # and return the length of the resulting list
        won: int = len([x for x in winners if x in all_numbers])

        # if won is at least 1, add 2 to the power of ("won"-1) to the result
        if won > 0:
            result += int(math.pow(2, won-1))

    return result


def add_scratchcard(processed: list, idx: int, how_many: int = 1) -> None:
    if len(processed) > idx:
        processed[idx] += how_many


def day04_part2(file_name: str, lines: int) -> int:
    # open the input file
    f: typing.TextIO = open(file_name, "r")

    processed: list = []
    # fill processed list with "lines" number of 1s
    for i in range(0, lines):
        processed.append(1)

    # read the input file, line by line
    for idx, line in enumerate(f):
        parsed_line: list = re.match(r"^Card\s+(\d+): (.*)\|(.*)$", line)
        winners: list = re.findall(r"\d+", parsed_line.groups()[1])
        all_numbers: list = re.findall(r"\d+", parsed_line.groups()[2])

        # find all elements of "winners" who are also present in "all_numbers"
        # and return the length of the resulting list
        won: int = len([x for x in winners if x in all_numbers])

        for i in range(1, won+1):
            add_scratchcard(processed, idx+i, processed[idx])

    # return sum of all the elements in "processed" list (which are ints)
    return sum(processed)


def test_day04_part1a():
    assert day04_part1("./input/day04a.txt") == 13


def test_day04_part1b():
    assert day04_part1("./input/day04b.txt") == 26218


def test_day04_part2a():
    assert day04_part2("./input/day04a.txt", 6) == 30


def test_day04_part2b():
    assert day04_part2("./input/day04b.txt", 201) == 9997537
