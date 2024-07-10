from enum import Enum, auto


class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()

    def __str__(self):
        if self is Direction.UP:
            return "UP"
        elif self is Direction.DOWN:
            return "DOWN"
        elif self is Direction.LEFT:
            return "LEFT"
        elif self is Direction.RIGHT:
            return "RIGHT"
        else:
            return "UNKNOWN"


class DirectedTile:
    def __init__(self, pos: tuple, direction: Direction):
        self.pos = pos
        self.direction = direction

    def __str__(self):
        return f"Pos: {self.pos}, Direction: {self.direction}"


class Maze:
    def __init__(self):
        self.maze = []
        self.start = None
        self.visited = {}
        self.trail = []

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

    def find_next(self, cur: tuple, prev: tuple) -> tuple:
        (i, j) = cur
        (k, l) = prev
        symbol = self.maze[i][j]
        if symbol == "|":
            if self.is_pos_legit(i-1, j) and (i-1, j) != (k, l):
                return DirectedTile((i-1, j), Direction.UP), cur
            if self.is_pos_legit(i+1, j) and (i+1, j) != (k, l):
                return DirectedTile((i+1, j), Direction.DOWN), cur
        elif symbol == "-":
            if self.is_pos_legit(i, j-1) and (i, j-1) != (k, l):
                return DirectedTile((i, j-1), Direction.LEFT), cur
            if self.is_pos_legit(i, j+1) and (i, j+1) != (k, l):
                return DirectedTile((i, j+1), Direction.RIGHT), cur
        elif symbol == "L":
            if self.is_pos_legit(i-1, j) and (i-1, j) != (k, l):
                return DirectedTile((i-1, j), Direction.UP), cur
            if self.is_pos_legit(i, j+1) and (i, j+1) != (k, l):
                return DirectedTile((i, j+1), Direction.RIGHT), cur
        elif symbol == "J":
            if self.is_pos_legit(i-1, j) and (i-1, j) != (k, l):
                return DirectedTile((i-1, j), Direction.UP), cur
            if self.is_pos_legit(i, j-1) and (i, j-1) != (k, l):
                return DirectedTile((i, j-1), Direction.LEFT), cur
        elif symbol == "7":
            if self.is_pos_legit(i+1, j) and (i+1, j) != (k, l):
                return DirectedTile((i+1, j), Direction.DOWN), cur
            if self.is_pos_legit(i, j-1) and (i, j-1) != (k, l):
                return DirectedTile((i, j-1), Direction.LEFT), cur
        elif symbol == "F":
            if self.is_pos_legit(i+1, j) and (i+1, j) != (k, l):
                return DirectedTile((i+1, j), Direction.DOWN), cur
            if self.is_pos_legit(i, j+1) and (i, j+1) != (k, l):
                return DirectedTile((i, j+1), Direction.RIGHT), cur

        return None, cur

    def find_two_paths(self) -> tuple:
        paths = []
        dirs = []
        (i, j) = self.start
        if self.is_pos_legit(i - 1, j) and self.maze[i - 1][j] in ("|", "7", "F"):
            paths.append((i - 1, j))
            dirs.append(Direction.UP)
        if self.is_pos_legit(i + 1, j) and self.maze[i + 1][j] in ("|", "L", "J"):
            paths.append((i + 1, j))
            dirs.append(Direction.DOWN)
        if self.is_pos_legit(i, j - 1) and self.maze[i][j - 1] in ("-", "L", "F"):
            paths.append((i, j - 1))
            dirs.append(Direction.LEFT)
        if self.is_pos_legit(i, j + 1) and self.maze[i][j + 1] in ("-", "7", "J"):
            paths.append((i, j + 1))
            dirs.append(Direction.RIGHT)

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

        return DirectedTile(paths[0], dirs[0]), DirectedTile(paths[1], dirs[1])

    def is_visited(self, pos: tuple) -> bool:
        return pos in self.visited.keys()

    def add_to_visited(self, pos: tuple, dist: int):
        self.visited[pos] = dist

    def add_to_trail(self, tile: DirectedTile):
        self.trail.append(tile)


def day10_part1(file_name: str) -> int:
    # read te maze from the file
    maze = Maze()
    maze.read_maze(file_name)

    # find the beginning of the maze
    dist = 0
    maze.find_start()
    # print(f"Start: {maze.start}")
    (tile1, tile2) = maze.find_two_paths()
    maze.add_to_visited(maze.start, dist)
    prev1 = maze.start
    prev2 = maze.start

    while True:
        # print(f"Path1: {path1}, Path2: {path2}")

        # traverse left and right end
        dist += 1
        maze.add_to_visited((tile1.pos[0], tile1.pos[1]), dist)
        maze.add_to_visited((tile2.pos[0], tile2.pos[1]), dist)

        (tile1, prev1) = maze.find_next(tile1.pos, prev1)
        if tile1 is None or maze.is_visited(tile1.pos):
            return dist

        (tile2, prev2) = maze.find_next(tile2.pos, prev2)
        if tile2 is None or maze.is_visited(tile2.pos):
            return dist


def add_to_lefties(maze: Maze, curr_idx: int, lefties: set) -> set:
    tile = maze.trail[curr_idx]
    (i, j) = (tile.pos[0], tile.pos[1])
    symbol = maze.maze[i][j]

    if symbol == "|":
        if tile.direction is Direction.UP and maze.is_pos_legit(i, j - 1) and not maze.is_visited((i, j - 1)):
            lefties.add((i, j - 1))
        elif tile.direction is Direction.DOWN and maze.is_pos_legit(i, j + 1) and not maze.is_visited((i, j + 1)):
            lefties.add((i, j + 1))
    elif symbol == "-":
        if tile.direction is Direction.LEFT and maze.is_pos_legit(i - 1, j) and not maze.is_visited((i - 1, j)):
            lefties.add((i - 1, j))
        elif tile.direction is Direction.RIGHT and maze.is_pos_legit(i + 1, j) and not maze.is_visited((i + 1, j)):
            lefties.add((i + 1, j))
    elif symbol == "L":
        if tile.direction is Direction.UP:
            if maze.is_pos_legit(i, j - 1) and not maze.is_visited((i, j - 1)):
                lefties.add((i, j - 1))
            if maze.is_pos_legit(i + 1, j - 1) and not maze.is_visited((i + 1, j - 1)):
                lefties.add((i + 1, j - 1))
            if maze.is_pos_legit(i + 1, j) and not maze.is_visited((i + 1, j)):
                lefties.add((i + 1, j))
    elif symbol == "J":
        if tile.direction is Direction.LEFT:
            if maze.is_pos_legit(i, j + 1) and not maze.is_visited((i, j + 1)):
                lefties.add((i, j + 1))
            if maze.is_pos_legit(i + 1, j + 1) and not maze.is_visited((i + 1, j + 1)):
                lefties.add((i + 1, j + 1))
            if maze.is_pos_legit(i + 1, j) and not maze.is_visited((i + 1, j)):
                lefties.add((i + 1, j))
    elif symbol == "7":
        if tile.direction is Direction.DOWN:
            if maze.is_pos_legit(i, j + 1) and not maze.is_visited((i, j + 1)):
                lefties.add((i, j + 1))
            if maze.is_pos_legit(i - 1, j + 1) and not maze.is_visited((i - 1, j + 1)):
                lefties.add((i - 1, j + 1))
            if maze.is_pos_legit(i - 1, j) and not maze.is_visited((i - 1, j)):
                lefties.add((i - 1, j))
    elif symbol == "F":
        if tile.direction is Direction.RIGHT:
            if maze.is_pos_legit(i, j - 1) and not maze.is_visited((i, j - 1)):
                lefties.add((i, j - 1))
            if maze.is_pos_legit(i - 1, j - 1) and not maze.is_visited((i - 1, j - 1)):
                lefties.add((i - 1, j - 1))
            if maze.is_pos_legit(i - 1, j) and not maze.is_visited((i - 1, j)):
                lefties.add((i - 1, j))

    return lefties


def add_to_righties(maze: Maze, curr_idx: int, righties: set) -> set:
    tile = maze.trail[curr_idx]
    (i, j) = (tile.pos[0], tile.pos[1])
    symbol = maze.maze[i][j]

    if symbol == "|":
        if tile.direction is Direction.DOWN and maze.is_pos_legit(i, j - 1) and not maze.is_visited((i, j - 1)):
            righties.add((i, j - 1))
        elif tile.direction is Direction.UP and maze.is_pos_legit(i, j + 1) and not maze.is_visited((i, j + 1)):
            righties.add((i, j + 1))
    elif symbol == "-":
        if tile.direction is Direction.RIGHT and maze.is_pos_legit(i - 1, j) and not maze.is_visited((i - 1, j)):
            righties.add((i - 1, j))
        elif tile.direction is Direction.LEFT and maze.is_pos_legit(i + 1, j) and not maze.is_visited((i + 1, j)):
            righties.add((i + 1, j))
    elif symbol == "L":
        if tile.direction is Direction.RIGHT:
            if maze.is_pos_legit(i, j - 1) and not maze.is_visited((i, j - 1)):
                righties.add((i, j - 1))
            if maze.is_pos_legit(i + 1, j - 1) and not maze.is_visited((i + 1, j - 1)):
                righties.add((i + 1, j - 1))
            if maze.is_pos_legit(i + 1, j) and not maze.is_visited((i + 1, j)):
                righties.add((i + 1, j))
    elif symbol == "J":
        if tile.direction is Direction.UP:
            if maze.is_pos_legit(i, j + 1) and not maze.is_visited((i, j + 1)):
                righties.add((i, j + 1))
            if maze.is_pos_legit(i + 1, j + 1) and not maze.is_visited((i + 1, j + 1)):
                righties.add((i + 1, j + 1))
            if maze.is_pos_legit(i + 1, j) and not maze.is_visited((i + 1, j)):
                righties.add((i + 1, j))
    elif symbol == "7":
        if tile.direction is Direction.LEFT:
            if maze.is_pos_legit(i, j + 1) and not maze.is_visited((i, j + 1)):
                righties.add((i, j + 1))
            if maze.is_pos_legit(i - 1, j + 1) and not maze.is_visited((i - 1, j + 1)):
                righties.add((i - 1, j + 1))
            if maze.is_pos_legit(i - 1, j) and not maze.is_visited((i - 1, j)):
                righties.add((i - 1, j))
    elif symbol == "F":
        if tile.direction is Direction.DOWN:
            if maze.is_pos_legit(i, j - 1) and not maze.is_visited((i, j - 1)):
                righties.add((i, j - 1))
            if maze.is_pos_legit(i - 1, j - 1) and not maze.is_visited((i - 1, j - 1)):
                righties.add((i - 1, j - 1))
            if maze.is_pos_legit(i - 1, j) and not maze.is_visited((i - 1, j)):
                righties.add((i - 1, j))

    return righties


def flood(maze: Maze, pos: tuple, flooded: set, touches_boundary: bool = False) -> tuple:
    (i, j) = pos
    for (i_, j_) in ((i - 1, j - 1),
                     (i - 1, j),
                     (i - 1, j + 1),
                     (i, j - 1),
                     (i, j + 1),
                     (i + 1, j - 1),
                     (i + 1, j),
                     (i + 1, j + 1)):
        if maze.is_pos_legit(i_, j_) and (i_, j_) not in flooded and not maze.is_visited((i_, j_)):
            if (i_ == 0 or i_ == len(maze.maze) - 1) or (j_ == 0 or j_ == len(maze.maze[i_]) - 1):
                touches_boundary = True
            flooded.add((i_, j_))
            (flooded, touches_boundary) = flood(maze, (i_, j_), flooded, touches_boundary)

    return flooded, touches_boundary


def day10_part2(file_name: str) -> int:
    # read the maze from the file
    maze = Maze()
    maze.read_maze(file_name)
    dist = 0
    maze.find_start()
    (tile, _) = maze.find_two_paths()
    maze.add_to_visited(maze.start, dist)
    maze.add_to_trail(DirectedTile(maze.start, tile.direction))
    prev = maze.start

    # traverse the whole maze, to collect the list of tiles
    while True:
        dist += 1
        maze.add_to_visited((tile.pos[0], tile.pos[1]), dist)

        (tile, prev) = maze.find_next(tile.pos, prev)
        maze.add_to_trail(DirectedTile(prev, tile.direction))
        if maze.is_visited(tile.pos):
            break

    # pick the direction, start traversing the maze
    print(f"Trail:")
    for tile in maze.trail:
        print(tile)

    lefties = set()
    righties = set()
    curr_idx = 0

    # collect tiles on the left and right separately
    while curr_idx < len(maze.trail):
        lefties = add_to_lefties(maze, curr_idx, lefties)
        righties = add_to_righties(maze, curr_idx, righties)
        curr_idx += 1

    # for the tiles on the left, use flooding algorithm
    new_lefties = set()
    for leftie in lefties:
        (new_lefties, touches_boundary) = flood(maze, leftie, new_lefties, False)

    if not touches_boundary:
        return len(new_lefties)

    # for the tiles on the right, use flooding algorithm
    new_righties = set()
    for rightie in righties:
        (new_righties, touches_boundary) = flood(maze, rightie, new_righties, False)

    if not touches_boundary:
        return len(new_righties)

    # things went veeeery bad
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
