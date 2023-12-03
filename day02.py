import typing
import re


def day02_part1(input_file: str, thresholds: (int, int, int)) -> int:
    # open the input file
    f: typing.TextIO = open(input_file, "r")
    result: int = 0

    # loop through the lines read from the file
    for line in f:
        # find all attempts in the line
        parsed: list = re.match(r"^Game (\d+): (.*)$", line)
        attempts: list = re.findall(r"[^;]+", parsed.groups()[1])

        max_used_red: int = 0
        max_used_green: int = 0
        max_used_blue: int = 0

        # iterate through all the groups in attempts
        for attempt in attempts:
            single_draw: list = re.compile(r"(\d+) (red|green|blue)")
            draws: list = single_draw.findall(attempt)
            for draw in draws:
                match draw[1]:
                    case "red":
                        max_used_red = max(max_used_red, int(draw[0]))
                    case "green":
                        max_used_green = max(max_used_green, int(draw[0]))
                    case "blue":
                        max_used_blue = max(max_used_blue, int(draw[0]))

        if max_used_red <= thresholds[0] and max_used_green <= thresholds[1] and max_used_blue <= thresholds[2]:
            result += int(parsed.groups()[0])

    return result


def test_day02_part1a():
    assert day02_part1("./input/day02a.txt", (12, 13, 14)) == 8

def test_day02_part1b():
    assert day02_part1("./input/day02b.txt", (12, 13, 14)) == 2683
