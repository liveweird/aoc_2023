import re
import typing
from typing import Callable


def get_seeds_part1(line: str) -> list:
    parsed_seeds: list = re.match(r"^seeds: (.+)$", line)
    return parsed_seeds.group(1).split(" ")


def get_seeds_part2(line: str) -> list:
    parsed_seeds: list = re.match(r"^seeds: (.+)$", line)
    singles: list = parsed_seeds.group(1).split(" ")
    pairs: list = list(zip(singles[::2], singles[1::2]))

    # create an empty set
    seeds: set = set()

    # iterate through each pair in pairs
    for pair in pairs:
        seeds = seeds.union(set(range(int(pair[0]), int(pair[0]) + int(pair[1]))))
        print(".")

    print("done")

    return list(seeds)


def day05_part1(file_name: str) -> int:
    return day05(file_name, get_seeds_part1)


def day05_part2(file_name: str) -> int:
    return day05(file_name, get_seeds_part2)


def day05(file_name: str, get_seeds: Callable[[str], int]) -> int:
    # open the input file
    f: typing.TextIO = open(file_name, "r")

    # read seeds line from the file
    line: str = f.readline()
    seeds = get_seeds(line)

    # read the empty line
    _ = f.readline()

    # create a list of empty lists
    mappings: list = []

    # read the section header
    line: str = f.readline()

    while line != "":
        parsed_header: list = re.match(r"^(\w+)-to-(\w+) map:$", line)
        from_name: str = parsed_header.group(1)
        to_name: str = parsed_header.group(2)
        mapping: list = []

        line = f.readline()

        # read line from file "f" until it's empty line or EOF
        while line != "" and line != "\n":
            parsed_line: list = re.match(r"^(\d+) (\d+) (\d+)$", line)
            dest_idx: int = int(parsed_line.group(1))
            source_idx: int = int(parsed_line.group(2))
            qty: int = int(parsed_line.group(3))
            mapping.append((source_idx, qty, dest_idx))
            line = f.readline()

        mappings.append(sorted(mapping, key=lambda trio: trio[0]))
        line = f.readline()

    subjects: list = []

    # go through all the seeds
    for seed in seeds:
        # go through all the mappings
        subject: int = int(seed)
        for mapping in mappings:
            # go through all the mapping rules
            for rule in mapping:
                # if the rule applies to the value, use it
                if rule[0] <= subject <= (rule[0] + rule[1] - 1):
                    subject = rule[2] + (subject - rule[0])
                    break

        # print the subject
        subjects.append(subject)

    return min(subjects)


def test_day05_part1a():
    assert day05_part1("./input/day05a.txt") == 35


def test_day05_part1b():
    assert day05_part1("./input/day05b.txt") == 31599214


def test_day05_part2a():
    assert day05_part2("./input/day05a.txt") == 46


def test_day05_part2b():
    assert day05_part2("./input/day05b.txt") == 46
