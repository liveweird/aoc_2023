import unittest
import re
from typing import List

from enum import Enum
class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

class Command:
    def __init__(self, direction: str, distance: int):
        if direction == "R":
            self.direction = Direction.RIGHT
        elif direction == "L":
            self.direction = Direction.LEFT
        elif direction == "U":
            self.direction = Direction.UP
        elif direction == "D":
            self.direction = Direction.DOWN
        self.distance = distance

    def __str__(self):
        return f"{self.direction} {self.distance}"

    def __repr__(self):
        return self.__str__()

class Position:
    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y

    def apply_command(self, command: Command) -> 'Position':
        if command.direction == Direction.RIGHT:
            return Position(self.x + command.distance, self.y)
        if command.direction == Direction.LEFT:
            return Position(self.x - command.distance, self.y)
        if command.direction == Direction.DOWN:
            return Position(self.x, self.y + command.distance)
        elif command.direction == Direction.UP:
            return Position(self.x, self.y - command.distance)

class Sequence:
    def __init__(self, direction: Direction, start: int, end: int):
        self.direction = direction
        self.start = start
        self.end = end

    def lower_bound(self):
        if self.direction == Direction.RIGHT or self.direction == Direction.DOWN:
            return self.start
        else:
            return self.end

    def upper_bound(self):
        if self.direction == Direction.RIGHT or self.direction == Direction.DOWN:
            return self.end
        else:
            return self.start

    def __str__(self):
        return f"{self.direction} {self.start} {self.end}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.direction == other.direction and self.start == other.start and self.end == other.end

    @staticmethod
    def wider_and_narrower(wider: 'Sequence', narrower: 'Sequence') -> (List['Sequence'], List['Sequence']):
        wider_split: List[Sequence] = []
        if wider.direction == Direction.RIGHT or wider.direction == Direction.DOWN:
            if wider.start != narrower.lower_bound():
                wider_split.append(Sequence(wider.direction, wider.start, narrower.lower_bound() - 1))
            wider_split.append(Sequence(wider.direction, narrower.lower_bound(), narrower.upper_bound()))
            if wider.end != narrower.upper_bound():
                wider_split.append(Sequence(wider.direction, narrower.upper_bound() + 1, wider.end))
        else:
            if wider.start != narrower.upper_bound():
                wider_split.append(Sequence(wider.direction, wider.start, narrower.upper_bound() + 1))
            wider_split.append(Sequence(wider.direction, narrower.upper_bound(), narrower.lower_bound()))
            if wider.end != narrower.lower_bound():
                wider_split.append(Sequence(wider.direction, narrower.lower_bound() - 1, wider.end))
        return wider_split, [narrower]

    @staticmethod
    def earlier_and_later(earlier: 'Sequence', later: 'Sequence') -> (List['Sequence'], List['Sequence']):
        earlier_split: List[Sequence] = []
        later_split: List[Sequence] = []
        ... # TODO
        return earlier_split, later_split

    @staticmethod
    def intersect(seq1: 'Sequence', seq2: 'Sequence') -> (List['Sequence'], List['Sequence']):
        # if the sequences are not intersecting, return them as they are
        if seq1.lower_bound() > seq2.upper_bound() or seq1.upper_bound() < seq2.lower_bound():
            return [seq1], [seq2]
        # if the sequences are equal, return them as they are
        if seq1.lower_bound() == seq2.lower_bound() and seq1.upper_bound() == seq2.upper_bound():
            return [seq1], [seq2]
        # if the 1st sequence contains the 2nd sequence, split the 1st sequence into 3 parts, but don't split the 2nd
        if seq1.lower_bound() <= seq2.lower_bound() and seq1.upper_bound() >= seq2.upper_bound():
            wider: Sequence = seq1
            narrower: Sequence = seq2
            (wider_split, narrower_split) = Sequence.wider_and_narrower(wider, narrower)
            return wider_split, narrower_split
        # if the 2nd sequence contains the 1st sequence, split the 2nd sequence into 3 parts, but don't split the 1st
        if seq2.lower_bound() <= seq1.lower_bound() and seq2.upper_bound() >= seq1.upper_bound():
            wider: Sequence = seq2
            narrower: Sequence = seq1
            (wider_split, narrower_split) = Sequence.wider_and_narrower(wider, narrower)
            return narrower_split, wider_split
        # if the 1st sequence starts before the 2nd sequence, split both sequences
        if seq1.lower_bound() < seq2.lower_bound():
            earlier: Sequence = seq1
            later: Sequence = seq2
            (earlier_split, later_split) = Sequence.earlier_and_later(earlier, later)
            return earlier_split, later_split
        # if the 2nd sequence starts before the 1st sequence, split both sequences
        if seq2.lower_bound() < seq1.lower_bound():
            earlier: Sequence = seq2
            later: Sequence = seq1
            (earlier_split, later_split) = Sequence.earlier_and_later(earlier, later)
            return later_split, earlier_split
        # if all conditions have failed, raise an exception
        raise Exception("Sequences are not intersecting")

class DigPlan:
    def __init__(self, file_name: str):
        with open(file_name, "r") as file:
            # read a line and parse it with a regular expression: one letter, space, one number, ignore the rest
            expr = re.compile(r"([A-Z]) (\d+)")
            self.commands: List[Command] = [Command(match.group(1), int(match.group(2))) for line in file for match in expr.finditer(line)]

        self.sequences: List[Sequence] = []

    def build_sequences(self):
        pos: Position = Position(0,0)

        for command in self.commands:
            new_pos: Position = pos.apply_command(command)
            seq: Sequence
            if pos.x != new_pos.x:
                seq = Sequence(command.direction, pos.x, new_pos.x)
            else:
                seq = Sequence(command.direction, pos.y, new_pos.y)
            pos = new_pos
            self.sequences.append(seq)

class Day18:
    @staticmethod
    def part1(file_name: str) -> int:
        plan = DigPlan(file_name)
        plan.build_sequences()

        for seq in plan.sequences:
            print(seq)

        # translate the dig plan from commands to sequences
        # analyze the sequences - separately horizontally and vertically
        # find intersecting sequences, split them into common ports
        # replace split sequences with small lists of sequences

        return 0

    @staticmethod
    def part2(file_name: str) -> int:
        return 0

class Tests(unittest.TestCase):
    def test_intersecting_sequences_no_intersection(self):
        seq1 = Sequence(Direction.RIGHT, 1, 3)
        seq2 = Sequence(Direction.RIGHT, 5, 7)
        (split1, split2) = Sequence.intersect(seq1, seq2)
        self.assertListEqual([seq1], split1)
        self.assertListEqual([seq2], split2)

    def test_intersecting_sequences_equal(self):
        seq1 = Sequence(Direction.RIGHT, 1, 3)
        seq2 = Sequence(Direction.RIGHT, 1, 3)
        (split1, split2) = Sequence.intersect(seq1, seq2)
        self.assertListEqual([seq1], split1)
        self.assertListEqual([seq2], split2)

    def test_intersecting_sequences_1_contains_2(self):
        seq1 = Sequence(Direction.RIGHT, 1, 7)
        seq2 = Sequence(Direction.RIGHT, 3, 5)
        (split1, split2) = Sequence.intersect(seq1, seq2)
        self.assertListEqual([Sequence(Direction.RIGHT, 1, 2), Sequence(Direction.RIGHT, 3, 5), Sequence(Direction.RIGHT, 6, 7)], split1)
        self.assertListEqual([seq2], split2)

    def test_intersecting_sequences_2_contains_1(self):
        seq1 = Sequence(Direction.RIGHT, 3, 5)
        seq2 = Sequence(Direction.RIGHT, 1, 7)
        (split1, split2) = Sequence.intersect(seq1, seq2)
        self.assertListEqual([seq1], split1)
        self.assertListEqual([Sequence(Direction.RIGHT, 1, 2), Sequence(Direction.RIGHT, 3, 5), Sequence(Direction.RIGHT, 6, 7)], split2)

    def test_intersecting_sequences_1_starts_before_2(self):
        seq1 = Sequence(Direction.RIGHT, 1, 3)
        seq2 = Sequence(Direction.RIGHT, 2, 4)
        (split1, split2) = Sequence.intersect(seq1, seq2)
        self.assertListEqual([Sequence(Direction.RIGHT, 1, 1), Sequence(Direction.RIGHT, 2, 3)], split1)
        self.assertListEqual([Sequence(Direction.RIGHT, 2, 3), Sequence(Direction.RIGHT, 4, 4)], split2)

    def test_intersecting_sequences_2_starts_before_1(self):
        seq1 = Sequence(Direction.RIGHT, 2, 4)
        seq2 = Sequence(Direction.RIGHT, 1, 3)
        (split1, split2) = Sequence.intersect(seq1, seq2)
        self.assertListEqual([Sequence(Direction.RIGHT, 2, 3), Sequence(Direction.RIGHT, 4, 4)], split2)
        self.assertListEqual([Sequence(Direction.RIGHT, 1, 1), Sequence(Direction.RIGHT, 2, 3)], split1)

    def test_day18_part1a(self):
        self.assertEqual(Day18.part1("input/day18a.txt"), 62)

    def test_day18_part1b(self):
        self.assertEqual(Day18.part1("input/day18b.txt"), 62)