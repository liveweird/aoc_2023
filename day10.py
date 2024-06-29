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

    def find_potential_neighbors(self, i: int, j: int) -> list:
        potentials = []
        symbol = self.maze[i][j]
        if symbol == "|":
            if self.is_pos_legit(i-1, j):
                potentials.append((i-1, j))
            if self.is_pos_legit(i+1, j):
                potentials.append((i+1, j))
        elif symbol == "-":
            if self.is_pos_legit(i, j-1):
                potentials.append((i, j-1))
            if self.is_pos_legit(i, j+1):
                potentials.append((i, j+1))
        elif symbol == "L":
            if self.is_pos_legit(i-1, j):
                potentials.append((i-1, j))
            if self.is_pos_legit(i, j+1):
                potentials.append((i, j+1))
        elif symbol == "J":
            if self.is_pos_legit(i-1, j):
                potentials.append((i-1, j))
            if self.is_pos_legit(i, j-1):
                potentials.append((i, j-1))
        elif symbol == "7":
            if self.is_pos_legit(i+1, j):
                potentials.append((i+1, j))
            if self.is_pos_legit(i, j-1):
                potentials.append((i, j-1))
        elif symbol == "F":
            if self.is_pos_legit(i+1, j):
                potentials.append((i+1, j))
            if self.is_pos_legit(i, j+1):
                potentials.append((i, j+1))
        return potentials

    def find_two_paths(self) -> tuple:
        paths = []
        (i, j) = self.start
        if self.is_pos_legit(i - 1, j) and self.maze[i - 1][j] in ("|", "7", "F"):
            paths.append((i - 1, j))
        if self.is_pos_legit(i + 1, j) and self.maze[i + 1][j] in ("|", "L", "J"):
            paths.append((i + 1, j))
        if self.is_pos_legit(i, j - 1) and self.maze[i][j - 1] in ("-", "L", "F"):
            paths.append((i, j - 1))
        if self.is_pos_legit(i, j + 1) and self.maze[i][j + 1] in ("-", "7", "J"):
            paths.append((i, j + 1))

        assert(len(paths) == 2)
        return paths[0], paths[1]

    def is_visited(self, pos: tuple) -> bool:
        return pos in self.visited.keys()

    def add_to_visited(self, pos: tuple, dist: int):
        self.visited[pos] = dist

    def filter_visited(self, potentials: list) -> list:
        return [pos for pos in potentials if not self.is_visited(pos)]


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
        maze.add_to_visited(path1, dist)
        maze.add_to_visited(path2, dist)

        pot1 = maze.find_potential_neighbors(path1[0], path1[1])
        next1 = maze.filter_visited(pot1)
        if len(next1) == 1:
            path1 = next1[0]
        else:
            return dist

        pot2 = maze.find_potential_neighbors(path2[0], path2[1])
        next2 = maze.filter_visited(pot2)
        if len(next2) == 1:
            path2 = next2[0]
        else:
            return dist


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
