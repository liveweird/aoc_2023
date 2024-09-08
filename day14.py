import unittest

class Plane:
    def __init__(self):
        self.sequences = []

    def add_sequence(self, sequence: str):
        self.sequences.append(sequence)

    def read_file(self, file_name: str):
        with open(file_name, "r") as file:
            for line in file:
                self.add_sequence(line.strip())

    def transpose(self):
        # transpose the matrix
        tuples = list(zip(*self.sequences))
        self.sequences = [''.join(t) for t in tuples]
    
    def mirror_vertical(self):
        self.sequences = self.sequences[::-1]

    def mirror_horizontal(self):
        self.sequences = [sequence[::-1] for sequence in self.sequences]

    def print(self):
        print()
        for sequence in self.sequences:
            print(sequence)
        print()

    def gravity_left(self):
        for sequence in self.sequences:
            # create new, empty sequence
            new_sequence = ""
            # start processing from the left
            idx = 0
            empty_count = 0
            rounded_count = 0
            while idx < len(sequence):
                if sequence[idx] == 'O':
                    rounded_count += 1
                elif sequence[idx] == '.':
                    empty_count += 1
                elif sequence[idx] == '#':
                    new_sequence += 'O' * rounded_count
                    new_sequence += '.' * empty_count
                    new_sequence += '#'
                    # reset the counters
                    rounded_count = 0
                    empty_count = 0
                else:
                    raise ValueError(f"Invalid character: {sequence[idx]}")
                idx += 1
            # add the number of 'O' characters before the first #
            new_sequence += 'O' * rounded_count
            new_sequence += '.' * empty_count
            self.sequences[self.sequences.index(sequence)] = new_sequence

    def calc_points(self, depth):
        points = 0
        for sequence in self.sequences:
            # find "O" characters and their indexes
            for idx, char in enumerate(sequence):
                if char == 'O':
                    points += (depth - idx)


        return points
    

class Day14:
    def part1(self, file_name: str, depth: int) -> int:
        plane = Plane()
        plane.read_file(file_name)
        plane.transpose()
        plane.gravity_left() 
        return plane.calc_points(depth)


class Tests(unittest.TestCase):
    def test_day14_part1a(self):
        self.assertEqual(Day14().part1("./input/day14a.txt", depth=10), 136)
 
    def test_day14_part1b(self):
        self.assertEqual(Day14().part1("./input/day14b.txt", depth=100), 136)


if __name__ == "__main__":
    unittest.main()