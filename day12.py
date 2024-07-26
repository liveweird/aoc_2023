from typing import List


class Puzzle:
    def __init__(self, to_process: str, sequences: List[int]):
        self.to_process = to_process
        self.sequences = sequences

    def strip_dots_left(self):
        self.to_process = self.to_process.lstrip(".")

    def __str__(self):
        return f"to_process: {self.to_process}, sequences: {self.sequences}"


def read_puzzles(file_name: str) -> List[Puzzle]:
    # create a puzzles list
    puzzles = []
    # open the file to read
    with open(file_name, "r") as file:
        # read the file
        for line in file:
            # split the line by the space character
            line = line.strip().split(" ")
            to_process = line[0]
            sequences = line[1].split(",")
            # convert the sequences to integers
            sequences = [int(sequence) for sequence in sequences]
            # create a new puzzle object
            puzzle = Puzzle(to_process, sequences)
            # add the puzzle to the puzzles list
            puzzles.append(puzzle)

    return puzzles


def count_combinations(puzzle: Puzzle) -> int:
    result = 0
    # print(puzzle)
    # strip the empty spaces (dots) from the left
    puzzle.strip_dots_left()
    # if the puzzle is empty, return 1 if the sequences are also empty, otherwise return 0
    if len(puzzle.to_process) == 0:
        if len(puzzle.sequences) == 0:
            # print("Good path")
            return 1
        else:
            # print("Bad path")
            return 0
    # if the first character is a question mark, run the same function with the first character removed
    if puzzle.to_process[0] == "?":
        result += count_combinations(Puzzle(puzzle.to_process[1:], puzzle.sequences))
    # assume the first character is a hash
    if len(puzzle.sequences) == 0:
        return result
    curr_sequence = puzzle.sequences[0]
    if len(puzzle.to_process) < curr_sequence:
        return result
    # check the first sequence, confirm if the sequence is possible
    if all(next_char in ("#", "?") for next_char in puzzle.to_process[:curr_sequence]) \
        and (len(puzzle.to_process) == curr_sequence \
             or (len(puzzle.to_process) > curr_sequence and puzzle.to_process[curr_sequence] in (".", "?"))):
        result += count_combinations(Puzzle(puzzle.to_process[curr_sequence+1:], puzzle.sequences[1:]))

    return result


def day12_part1(file_name: str) -> int:
    puzzles = read_puzzles(file_name)

    # process puzzles, one by one
    result = 0
    for puzzle in puzzles:
        result += count_combinations(puzzle)

    return result


def expand_puzzles(puzzles):
    expanded_puzzles = []
    for puzzle in puzzles:
        to_process = "?".join([puzzle.to_process] * 5)
        sequences = puzzle.sequences * 5
        expanded_puzzles.append(Puzzle(to_process, sequences))

    return expanded_puzzles


def day12_part2(file_name: str) -> int:
    puzzles = read_puzzles(file_name)
    expanded_puzzles = expand_puzzles(puzzles)

    # process puzzles, one by one
    result = 0
    for puzzle in expanded_puzzles:
        # print(puzzle)
        result += count_combinations(puzzle)

    return result


def test_day12_part1a() -> None:
    assert day12_part1("./input/day12a.txt") == 21


def test_day12_part1b() -> None:
    assert day12_part1("./input/day12b.txt") == 7506


def test_day12_part1c() -> None:
    assert day12_part2("./input/day12a.txt") == 525152


def test_day12_part1d() -> None:
    assert day12_part2("./input/day12b.txt") == 525152