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


def is_gear(suspect: str) -> bool:
    return suspect == "*"


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


def add_to_gear(gears: dict, line_no: int, pos: int, number: int) -> None:
    if (line_no, pos) in gears:
        gears[(line_no, pos)].append(number)
    else:
        gears[(line_no, pos)] = [number]


def search_for_gears(input: list, line_no: int, start_pos: int, end_pos: int, gears: dict) -> None:
    # line before
    if line_no > 0:
        for x in range(start_pos - 1, end_pos + 2):
            if 0 <= x < len(input[line_no - 1]):
                if is_gear(input[line_no - 1][x]):
                    add_to_gear(gears, line_no - 1, x, calc_number(input[line_no], start_pos, end_pos))

    # line after
    if line_no < len(input) - 1:
        for x in range(start_pos - 1, end_pos + 2):
            if 0 <= x < len(input[line_no - 1]):
                if is_gear(input[line_no + 1][x]):
                    add_to_gear(gears, line_no + 1, x, calc_number(input[line_no], start_pos, end_pos))

    # char to the left
    if 1 <= start_pos:
        if is_gear(input[line_no][start_pos - 1]):
            add_to_gear(gears, line_no, start_pos - 1, calc_number(input[line_no], start_pos, end_pos))

    # char to the right
    if end_pos < len(input[line_no]) - 2:
        if is_gear(input[line_no][end_pos + 1]):
            add_to_gear(gears, line_no, end_pos + 1, calc_number(input[line_no], start_pos, end_pos))


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


def day03_part2(input_file: str) -> int:
    # open the input file
    f: typing.TextIO = open(input_file, "r")

    # load the input file content into 2-dimensional array
    input: list = []
    for line in f:
        input.append(list(line.strip()))

    # create an empty map, indexed with gear coordinates, the value is list of ints
    gears: dict = {}

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
                    search_for_gears(input, line_no, start_pos, end_pos, gears)

        if mode == Mode.DIGIT:
            mode = Mode.NO_DIGIT
            end_pos = len(line) - 1
            search_for_gears(input, line_no, start_pos, end_pos, gears)

        line_no += 1

    # for all elements of gears dictionary, that have a value with exactly two elements,
    # sum up the product of these two elements
    result: int = 0
    for key in gears:
        if len(gears[key]) == 2:
            result += gears[key][0] * gears[key][1]

    return result


def test_day03_part1a():
    assert day03_part1("input/day03a.txt") == 4361

def test_day03_part1b():
    assert day03_part1("input/day03b.txt") == 521601

def test_day03_part2a():
    assert day03_part2("input/day03a.txt") == 467835

def test_day03_part2b():
    assert day03_part2("input/day03b.txt") == 80694070
