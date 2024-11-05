import unittest
import re

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

class DigPlan:
    def __init__(self, file_name: str):
        with open(file_name, "r") as file:
            # read a line and parse it with a regular expression: one letter, space, one number, ignore the rest
            expr = re.compile(r"([A-Z]) (\d+)")
            self.commands = [Command(match.group(1), int(match.group(2))) for line in file for match in expr.finditer(line)]

        print(self.commands)

class Day18:
    @staticmethod
    def part1(file_name: str) -> int:
        plan = DigPlan(file_name)
        return 0

    @staticmethod
    def part2(file_name: str) -> int:
        return 0

class Tests(unittest.TestCase):
    def test_day18_part1a(self):
        self.assertEqual(Day18.part1("input/day18a.txt"), 62)

    def test_day18_part1b(self):
        self.assertEqual(Day18.part1("input/day18b.txt"), 62)