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


def get_left_digit(line: str) -> int:
    # find index of the first digit in the line
    pattern_left: str = r"^\D*(\d)"

    # if there is any digit in the line, then find its index
    if re.search(pattern_left, line):
        first_digit_index: int = re.search(pattern_left, line).start(1)
        first_digit: int = int(line[first_digit_index])
    else:
        # otherwise, set first_digit_index to 1000
        first_digit_index: int = 1000
        first_digit: int = 1000

    # create a list with all digits from zero to nine, but in textual form
    digits: list = [r"zero", r"one", r"two", r"three", r"four", r"five", r"six", r"seven", r"eight", r"nine"]

    # iterate through the digits from the list above
    first_digit_indices: list = []
    for digit in digits:
        # if the digit is found in the line, then append the index of its first occurrence to the list
        if re.search(digit, line):
            first_digit_indices.append(re.search(digit, line).start(0))
            # otherwise, append 1000 to the list
        else:
            first_digit_indices.append(1000)

    # find the lowest value in the list of indices, and its index in the list
    lowest_index: int = min(first_digit_indices)
    lowest_index_index: int = first_digit_indices.index(lowest_index)

    # if first_digit_index is lower than lowest_index, then set left_digit to first_digit
    if first_digit_index < lowest_index:
        left_digit: int = first_digit
    else:
        # otherwise, set left_digit to lowest_index_index
        left_digit: int = lowest_index_index

    return left_digit


def get_right_digit(line: str) -> int:
    # find index of the last digit in the line
    pattern_right: str = r"(\d)\D*$"

    # if there is any digit in the line, then find its index
    if re.search(pattern_right, line):
        last_digit_index: int = re.search(pattern_right, line).start(1)
        last_digit: int = int(line[last_digit_index])
    else:
        # otherwise, set last_digit_index to -1
        last_digit_index: int = -1
        last_digit: int = -1

    # create a list with all digits from zero to nine, but in textual form
    digits: list = [r"zero", r"one", r"two", r"three", r"four", r"five", r"six", r"seven", r"eight", r"nine"]

    # iterate through the digits from the list above
    last_digit_indices: list = []
    for digit in digits:
        # if the digit is found in the line, then append the index of its last occurrence to the list
        if re.search(digit, line):
            *_, last = re.finditer(digit, line)
            last_digit_indices.append(last.start(0))
            # otherwise, append -1 to the list
        else:
            last_digit_indices.append(-1)

    # find the highest value in the list of indices, and its index in the list
    highest_index: int = max(last_digit_indices)
    highest_index_index: int = last_digit_indices.index(highest_index)

    # if last_digit_index is higher than highest_index, then set right_digit to last_digit
    if last_digit_index > highest_index:
        right_digit: int = last_digit
    else:
        # otherwise, set right_digit to highest_index_index
        right_digit: int = highest_index_index

    return right_digit


def day01_part2(input_file: str) -> int:
    # open the input file
    f: typing.TextIO = open(input_file, "r")
    total: int = 0

    # loop through the lines read from the file
    for line in f:

        # get left digit
        left_digit: int = get_left_digit(line)
        right_digit: int = get_right_digit(line)

        # make a single number out of these two digits
        to_be_added: int = left_digit * 10 + right_digit

        # add this number to the total
        total += to_be_added

    # return the total
    return total


def test_day01_part1a():
    assert day01_part1("./input/day01a.txt") == 142


def test_day01_part1b():
    assert day01_part1("./input/day01b.txt") == 56397


def test_day01_part2c():
    assert day01_part2("./input/day01c.txt") == 281


def test_day01_part2b():
    assert day01_part2("./input/day01b.txt") == 55701
