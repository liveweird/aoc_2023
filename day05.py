import re
import typing
from typing import Callable


def get_seeds_part1(line: str) -> list:
    parsed_seeds: list = re.match(r"^seeds: (.+)$", line)
    strings: list = parsed_seeds.group(1).split(" ")

    # convert the list of strings into the list of ints
    seeds: list = list(map(int, strings))
    return seeds


def get_seeds_part2(line: str) -> list:
    parsed_seeds: list = re.match(r"^seeds: (.+)$", line)
    singles: list = parsed_seeds.group(1).split(" ")
    pairs: list = list(zip(singles[::2], singles[1::2]))

    # create an empty set
    seeds: set = set()

    # iterate through each pair in pairs
    for pair in pairs:
        seeds = seeds.union(set(range(int(pair[0]), int(pair[0]) + int(pair[1]))))

    return list(seeds)


def in_seeds_part1(line: str, checked: int) -> bool:
    parsed_seeds: list = re.match(r"^seeds: (.+)$", line)
    strings: list = parsed_seeds.group(1).split(" ")

    # convert the list of strings into the list of ints
    seeds: list = list(map(int, strings))
    return checked in seeds


def in_seeds_part2(line: str, checked: int) -> bool:
    parsed_seeds: list = re.match(r"^seeds: (.+)$", line)
    singles: list = parsed_seeds.group(1).split(" ")
    pairs: list = list(zip(singles[::2], singles[1::2]))

    # get the pairs sorted by the first element
    pairs = sorted(pairs, key=lambda sorted_pair: int(sorted_pair[0]))

    # iterate through each pair in pairs
    for pair in pairs:
        # if the checked number is in the range of the pair, return True
        if int(pair[0]) <= checked <= int(pair[0]) + int(pair[1]):
            return True

    return False


def day05_part1(file_name: str) -> int:
    return day05b(file_name, in_seeds_part1)


def day05_part2(file_name: str) -> int:
    return day05b(file_name, in_seeds_part2)


def day05a(file_name: str, get_seeds: Callable[[str], int]) -> int:
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
        subject: int = seed
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


def day05b(file_name: str, in_seeds: Callable[[str, int], int]) -> int:
    # open the input file
    f: typing.TextIO = open(file_name, "r")

    # read seeds line from the file
    seed_line: str = f.readline()

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

        mappings.append(sorted(mapping, key=lambda trio: trio[2]))
        line = f.readline()

    idx: int = 0

    # go through all the tuples in the final_mapping
    while True:
        subject: int = idx

        # go through all the mappings, in the reverse order
        for mapping in reversed(mappings):
            # go through all the mapping rules
            for rule in mapping:
                # if the rule applies to the value, use it
                if rule[2] <= subject <= (rule[2] + rule[1] - 1):
                    subject = rule[0] + (subject - rule[2])
                    break

        # if the subject is in the seeds, return it
        if in_seeds(seed_line, subject):
            return idx

        idx += 1


def test_day05_part1a():
    assert day05_part1("./input/day05a.txt") == 35


def test_day05_part1b():
    assert day05_part1("./input/day05b.txt") == 31599214


def test_day05_part2a():
    assert day05_part2("./input/day05a.txt") == 46


def test_day05_part2b():
    assert day05_part2("./input/day05b.txt") == 20358599
