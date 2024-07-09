from enum import Enum, auto


class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


class Maze:
    def __init__(self):
        self.maze = []
        self.start = None
        self.visited = {}

    def read_maze(self, file_name: str):
        with open(file_name, "r") as f:
            for line in f:
                self.maze.append(list(line.strip()))

    def print_maze(self):
        for row in self.maze:
            print("".join(row))

    def find_start(self):
        for i in range(len(self.maze)):
            for j in range(len(self.maze[i])):
                if self.maze[i][j] == "S":
                    self.start = (i, j)
                    return

    def is_pos_legit(self, i: int, j: int) -> bool:
        if i < 0 or i >= len(self.maze):
            return False
        if j < 0 or j >= len(self.maze[i]):
            return False
        return True

    def find_next(self, i: int, j: int) -> tuple:
        symbol = self.maze[i][j]
        if symbol == "|":
            if self.is_pos_legit(i-1, j) and not self.is_visited((i-1, j)):
                return i-1, j, Direction.UP
            if self.is_pos_legit(i+1, j) and not self.is_visited((i+1, j)):
                return i+1, j, Direction.DOWN
        elif symbol == "-":
            if self.is_pos_legit(i, j-1) and not self.is_visited((i, j-1)):
                return i, j-1, Direction.LEFT
            if self.is_pos_legit(i, j+1) and not self.is_visited((i, j+1)):
                return i, j+1, Direction.RIGHT
        elif symbol == "L":
            if self.is_pos_legit(i-1, j) and not self.is_visited((i-1, j)):
                return i-1, j, Direction.UP
            if self.is_pos_legit(i, j+1) and not self.is_visited((i, j+1)):
                return i, j+1, Direction.RIGHT
        elif symbol == "J":
            if self.is_pos_legit(i-1, j) and not self.is_visited((i-1, j)):
                return i-1, j, Direction.UP
            if self.is_pos_legit(i, j-1) and not self.is_visited((i, j-1)):
                return i, j-1, Direction.LEFT
        elif symbol == "7":
            if self.is_pos_legit(i+1, j) and not self.is_visited((i+1, j)):
                return i+1, j, Direction.DOWN
            if self.is_pos_legit(i, j-1) and not self.is_visited((i, j-1)):
                return i, j-1, Direction.LEFT
        elif symbol == "F":
            if self.is_pos_legit(i+1, j) and not self.is_visited((i+1, j)):
                return i+1, j, Direction.DOWN
            if self.is_pos_legit(i, j+1) and not self.is_visited((i, j+1)):
                return i, j+1, Direction.RIGHT

        return ()

    def find_two_paths(self) -> tuple:
        paths = []
        dirs = set()
        (i, j) = self.start
        if self.is_pos_legit(i - 1, j) and self.maze[i - 1][j] in ("|", "7", "F"):
            paths.append((i - 1, j))
            dirs.add(Direction.UP)
        if self.is_pos_legit(i + 1, j) and self.maze[i + 1][j] in ("|", "L", "J"):
            paths.append((i + 1, j))
            dirs.add(Direction.DOWN)
        if self.is_pos_legit(i, j - 1) and self.maze[i][j - 1] in ("-", "L", "F"):
            paths.append((i, j - 1))
            dirs.add(Direction.LEFT)
        if self.is_pos_legit(i, j + 1) and self.maze[i][j + 1] in ("-", "7", "J"):
            paths.append((i, j + 1))
            dirs.add(Direction.RIGHT)

        assert len(paths) == 2

        # replace the start with the correct symbol
        if Direction.LEFT in dirs and Direction.RIGHT in dirs:
            self.maze[i][j] = "-"
        elif Direction.UP in dirs and Direction.DOWN in dirs:
            self.maze[i][j] = "|"
        elif Direction.LEFT in dirs and Direction.UP in dirs:
            self.maze[i][j] = "J"
        elif Direction.LEFT in dirs and Direction.DOWN in dirs:
            self.maze[i][j] = "7"
        elif Direction.RIGHT in dirs and Direction.UP in dirs:
            self.maze[i][j] = "L"
        elif Direction.RIGHT in dirs and Direction.DOWN in dirs:
            self.maze[i][j] = "F"
        else:
            assert False

        return paths[0], paths[1]

    def is_visited(self, pos: tuple) -> bool:
        return pos in self.visited.keys()

    def add_to_visited(self, pos: tuple, dist: int):
        self.visited[pos] = dist


def day10_part1(file_name: str) -> int:
    # read te maze from the file
    maze = Maze()
    maze.read_maze(file_name)

    # find the beginning of the maze
    dist = 0
    maze.find_start()
    # print(f"Start: {maze.start}")
    maze.add_to_visited(maze.start, dist)
    (path1, path2) = maze.find_two_paths()

    while True:
        # print(f"Path1: {path1}, Path2: {path2}")

        # traverse left and right end
        dist += 1
        maze.add_to_visited((path1[0], path1[1]), dist)
        maze.add_to_visited((path2[0], path2[1]), dist)

        path1 = maze.find_next(path1[0], path1[1])
        if len(path1) == 0:
            return dist

        path2 = maze.find_next(path2[0], path2[1])
        if len(path2) == 0:
            return dist


def day10_part2(file_name: str) -> int:
    # read the maze from the file
    maze = Maze()
    maze.read_maze(file_name)
    dist = 0
    maze.find_start()
    maze.add_to_visited(maze.start, dist)
    (path, _) = maze.find_two_paths()

    # traverse the whole maze, to collect the list of tiles
    while True:
        dist += 1
        maze.add_to_visited(path, dist)

        path = maze.find_next(path[0], path[1])
        if len(path) == 0:
            break

    # pick the direction, start traversing the maze
    lefties = set()
    righties = set()
    prev = len(maze.visited) - 1
    curr = 0

    # collect tiles on the left and right separately
    # for the tiles on the left, use flooding algorithm
    # for the tiles on the right, use flooding algorithm
    # return the size of the set of the tiles that doesn't touch boundaries
    return 0


def test_day10_part1a():
    assert day10_part1("./input/day10a.txt") == 4


def test_day10_part1b():
    assert day10_part1("./input/day10b.txt") == 4


def test_day10_part1c():
    assert day10_part1("./input/day10c.txt") == 8


def test_day10_part1d():
    assert day10_part1("./input/day10d.txt") == 8


def test_day10_part1e():
    assert day10_part1("./input/day10e.txt") == 6942


def test_day10_part2a():
    assert day10_part2("./input/day10f.txt") == 4


def test_day10_part2b():
    assert day10_part2("./input/day10g.txt") == 8


def test_day10_part2c():
    assert day10_part2("./input/day10h.txt") == 10