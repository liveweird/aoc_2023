import typing
import math
from enum import Enum


class Mode(Enum):
    NO_DIGIT = 0,
    DIGIT = 1


def calc_number(line: list, start_pos: int, end_pos: int) -> int:
    result: int = 0
    for x in range(start_pos, end_pos + 1):
        result += int(line[x]) * int(math.pow(10, (end_pos - x)))
    return result


def is_symbol(suspect: str) -> bool:
    return not suspect.isdigit() and not suspect == "."


def check_number(input: list, line_no: int, start_pos: int, end_pos: int) -> bool:
    # line before
    if line_no > 0:
        for x in range(start_pos - 1, end_pos + 2):
            if 0 <= x < len(input[line_no - 1]):
                if is_symbol(input[line_no - 1][x]):
                    return True

    # line after
    if line_no < len(input) - 1:
        for x in range(start_pos - 1, end_pos + 2):
            if 0 <= x < len(input[line_no - 1]):
                if is_symbol(input[line_no + 1][x]):
                    return True

    # char to the left
    if 1 <= start_pos:
        if is_symbol(input[line_no][start_pos - 1]):
            return True

    # char to the right
    if end_pos < len(input[line_no]) - 2:
        if is_symbol(input[line_no][end_pos + 1]):
            return True

    return False


def day03_part1(input_file: str) -> int:
    # open the input file
    f: typing.TextIO = open(input_file, "r")

    # load the input file content into 2-dimensional array
    input: list = []
    for line in f:
        input.append(list(line.strip()))

    result: int = 0
    line_no: int = 0
    # iterate through the input, line by line
    for line in input:
        mode: Mode = Mode.NO_DIGIT
        start_pos: int = 0
        end_pos: int = 0
        for x in range(len(line)):
            if mode == Mode.NO_DIGIT:
                if line[x].isdigit():
                    mode = Mode.DIGIT
                    start_pos = x
                else:
                    continue
            else:
                if line[x].isdigit():
                    continue
                else:
                    mode = Mode.NO_DIGIT
                    end_pos = x - 1
                    if check_number(input, line_no, start_pos, end_pos):
                        result += calc_number(line, start_pos, end_pos)

        if mode == Mode.DIGIT:
            mode = Mode.NO_DIGIT
            end_pos = len(line) - 1
            if check_number(input, line_no, start_pos, end_pos):
                result += calc_number(line, start_pos, end_pos)

        line_no += 1

    return result


def test_day03_part1a():
    assert day03_part1("input/day03a.txt") == 4361

def test_day03_part1b():
    assert day03_part1("input/day03b.txt") == 521601
