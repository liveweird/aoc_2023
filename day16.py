import unittest

class DIRECTION:
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def __str__(self):
        return str(self)

class Ray:
    def __init__(self, position: tuple = (-1, 0), direction: DIRECTION = DIRECTION.RIGHT) -> None:
        self.position = position
        self.direction = direction

    def move(self, floor: any) -> list:
        # get next tile for this ray
        x, y = self.position
        if self.direction == DIRECTION.UP:
            y -= 1
        elif self.direction == DIRECTION.RIGHT:
            x += 1
        elif self.direction == DIRECTION.DOWN:
            y += 1
        elif self.direction == DIRECTION.LEFT:
            x -= 1
        
        # check if we are not out of bounds
        if x < 0 or x >= len(floor.grid[0]) or y < 0 or y >= len(floor.grid):
            return []

        tile = floor.get_tile(x, y)

        # interpret the new tile
        if tile == '.':
            return [Ray((x, y), self.direction)]
        elif tile == '/':
            if self.direction == DIRECTION.UP:
                return [Ray((x, y), DIRECTION.RIGHT)]
            elif self.direction == DIRECTION.RIGHT:
                return [Ray((x, y), DIRECTION.UP)]
            elif self.direction == DIRECTION.DOWN:
                return [Ray((x, y), DIRECTION.LEFT)]
            elif self.direction == DIRECTION.LEFT:
                return [Ray((x, y), DIRECTION.DOWN)]
        elif tile == '\\':
            if self.direction == DIRECTION.UP:
                return [Ray((x, y), DIRECTION.LEFT)]
            elif self.direction == DIRECTION.RIGHT:
                return [Ray((x, y), DIRECTION.DOWN)]
            elif self.direction == DIRECTION.DOWN:
                return [Ray((x, y), DIRECTION.RIGHT)]
            elif self.direction == DIRECTION.LEFT:
                return [Ray((x, y), DIRECTION.UP)]
        elif tile == '|':
            if self.direction == DIRECTION.UP or self.direction == DIRECTION.DOWN:
                return [Ray((x, y), self.direction)]
            else:
                return [Ray((x, y), DIRECTION.UP), Ray((x, y), DIRECTION.DOWN)]
        elif tile == '-':
            if self.direction == DIRECTION.LEFT or self.direction == DIRECTION.RIGHT:
                return [Ray((x, y), self.direction)]
            else:
                return [Ray((x, y), DIRECTION.LEFT), Ray((x, y), DIRECTION.RIGHT)]

    def __eq__(self, other):
        return self.position == other.position and self.direction == other.direction

    def __hash__(self):
        return hash((self.position, self.direction))

    def __str__(self):
        return f"Ray: {self.position} {self.direction}"

class Floor:
    def __init__(self):
        self.grid = []
        self.rays: list[Ray] = [ Ray() ]

    def load(self, file_name: str):
        with open(file_name) as f:
            for line in f:
                self.grid.append(list(line.strip()))

    def get_tile(self, x: int, y: int):
        return self.grid[y][x]

    def __str__(self):
        return str(self.grid)

class Day16:
    @staticmethod
    def print_energized(energized: set):
        for y in range(0, 10):
            for x in range(0, 10):
                if (x, y) in energized:
                    print("#", end="")
                else:
                    print(".", end="")
            print()

    @staticmethod
    def part1(file_name: str):
        floor = Floor()
        floor.load(file_name)
        rays = floor.rays
        energized = set()
        history = set()

        while len(rays) > 0:
            new_rays: list[Ray] = []
            for ray in rays:
                temp_rays = ray.move(floor)
                for temp_ray in temp_rays:
                    energized.add(temp_ray.position)
                    if temp_ray not in history:
                        history.add(temp_ray)
                        new_rays.append(temp_ray)
            rays = new_rays

        # Day16.print_energized(energized)
        return len(energized)

    @staticmethod
    def part2(file_name: str):
        return 0

class Tests(unittest.TestCase):
    def test_day16_part1a(self):
        self.assertEqual(Day16.part1("input/day16a.txt"), 10)

    def test_day16_part1b(self):
        self.assertEqual(Day16.part1("input/day16b.txt"), 46)

    def test_day16_part1c(self):
        self.assertEqual(Day16.part1("input/day16c.txt"), 8034)

if __name__ == "__main__":
    unittest.main()