import typing
import re


def day01_part1(input_file: str) -> int:
    # open the input file
    f: typing.TextIO = open(input_file, "r")
    total: int = 0

    # loop through the lines read from the file
    for line in f:

        # for each line, find the first digit and the last digit
        pattern_left: str = r"^\D*(\d)"
        pattern_right: str = r"(\d)\D*$"
        first_digit: int = int(re.search(pattern_left, line).group(1))
        last_digit: int = int(re.search(pattern_right, line).group(1))

        # make a single number out of these two digits
        to_be_added: int = first_digit * 10 + last_digit

        # add this number to the total
        total += to_be_added

    # return the total
    return total


def test_day01_part1a():
    assert day01_part1("./input/day01a.txt") == 142


def test_day01_part1b():
    assert day01_part1("./input/day01b.txt") == 56397

