import unittest


class Day16:
    @staticmethod
    def part1(file_name: str):
        return 0

    @staticmethod
    def part2(file_name: str):
        return 0

class Tests(unittest.TestCase):
    def test_day16_part1a(self):
        self.assertEqual(Day16.part1("./input/day16a.txt"), 46)

    def test_day16_part1b(self):
        self.assertEqual(Day16.part1("./input/day16b.txt"), 46)

if __name__ == "__main__":
    unittest.main()