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

    def __str__(self):
        return f"{self.direction} {self.start} {self.end}"

    def __repr__(self):
        return self.__str__()

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
    def test_day18_part1a(self):
        self.assertEqual(Day18.part1("input/day18a.txt"), 62)

    def test_day18_part1b(self):
        self.assertEqual(Day18.part1("input/day18b.txt"), 62)