import unittest
from typing import List


class Day15:
    @staticmethod
    def calc_hash(sequence: str) -> int:
        result = 0
        # for every character in the sequence ...
        for char in sequence:
            # get the ASCII code of the char
            ascii_code = ord(char)
            result += ascii_code
            result *= 17
            # get the remainder of the division by 256
            result %= 256

        return result

    def part1(self, file_name: str) -> int:
        result = 0
        # open the file_name file & read the single line
        with open(file_name, "r") as file:
            line = file.readline().strip()

            # split the line by commas
            sequences: list[str] = list(line.split(","))

            # for every sequence, calculate the hash
            for sequence in sequences:
                hashed = self.calc_hash(sequence)

                # sum all the hashes & return them
                result += hashed

        return result

    def part2(self, file_name: str) -> int:
        return 0

class Tests(unittest.TestCase):
    def test_day15_part1a(self):
        self.assertEqual(Day15().part1("./input/day15a.txt"), 52)

    def test_day15_part1b(self):
        self.assertEqual(Day15().part1("./input/day15b.txt"), 1320)

    def test_day15_part1c(self):
        self.assertEqual(Day15().part1("./input/day15c.txt"), 510013)

if __name__ == '__main__':
    unittest.main()