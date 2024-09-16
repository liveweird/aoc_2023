import unittest
from contextlib import nullcontext


class Plane:
    def __init__(self):
        self.sequences = []
        self.cache = {}
        self.route = {}
        self.points = {}

    def add_sequence(self, sequence: str):
        self.sequences.append(sequence)

    def read_file(self, file_name: str):
        with open(file_name, "r") as file:
            for line in file:
                self.add_sequence(line.strip())

    def copy(self):
        new_plane = Plane()
        new_plane.sequences = self.sequences.copy()
        new_plane.cache = self.cache.copy()
        return new_plane

    def create_hash(self) -> int:
        return hash(tuple(self.sequences))

    def add_to_route(self, prev_hash: int) -> int:
        # create a hash of the current state of the plane
        curr_hash = self.create_hash()
        # if prev_hash is not in the map, add it
        if prev_hash not in self.route:
            self.route[prev_hash] = curr_hash
        return curr_hash

    def print_diff(self, other):
        # print the number of sequences that are different
        diffs = []
        for idx, sequence in enumerate(self.sequences):
            if sequence != other.sequences[idx]:
                diffs.append(idx)
        print(f"Different sequences: {diffs}")

    def transpose(self):
        # transpose the matrix
        tuples = list(zip(*self.sequences))
        self.sequences = [''.join(t) for t in tuples]
    
    def mirror_vertical(self):
        self.sequences = self.sequences[::-1]

    def mirror_horizontal(self):
        self.sequences = [sequence[::-1] for sequence in self.sequences]

    def rotate_90CW(self):
        self.transpose()
        self.mirror_horizontal()

    def rotate_90CCW(self):
        self.transpose()
        self.mirror_vertical()

    def print(self):
        print()
        for sequence in self.sequences:
            print(sequence)
        print()

    def gravity_left(self):
        for sequence in self.sequences:
            # if sequence is a key in cache, set new_sequence to the corresponding value
            if sequence in self.cache:
                new_sequence = self.cache[sequence]
            else:
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
                # add the sequence to the cache
                self.cache[sequence] = new_sequence

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
        plane.rotate_90CCW()
        plane.gravity_left() 
        return plane.calc_points(depth)
    
    def part2(self, file_name: str, depth: int) -> int:
        plane = Plane()
        plane.read_file(file_name)
        plane.rotate_90CCW()
        curr_hash = plane.create_hash()
        route_entered = False

        for _ in range(1_000_000_000):
            if curr_hash in plane.route:
                # if the hash is already in the map, get the successor
                curr_hash = plane.route[curr_hash]
                route_entered = True
            else:
                assert route_entered == False
                plane.gravity_left()
                plane.rotate_90CW()
                plane.gravity_left()
                plane.rotate_90CW()
                plane.gravity_left()
                plane.rotate_90CW()
                plane.gravity_left()
                plane.rotate_90CW()
                curr_hash = plane.add_to_route(curr_hash)
                plane.points[curr_hash] = plane.calc_points(depth)

        print(plane.route)

        return plane.points[curr_hash]


class Tests(unittest.TestCase):
    def test_day14_part1a(self):
        self.assertEqual(Day14().part1("./input/day14a.txt", depth=10), 136)
 
    def test_day14_part1b(self):
        self.assertEqual(Day14().part1("./input/day14b.txt", depth=100), 105982)

    def test_day14_part1c(self):
        self.assertEqual(Day14().part2("./input/day14a.txt", depth=10), 64)

    def test_day14_part1d(self):
        self.assertEqual(Day14().part2("./input/day14b.txt", depth=100), 85175)

if __name__ == "__main__":
    unittest.main()