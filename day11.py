class Galaxy:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self):
        return f"Galaxy: {self.x}, {self.y}"


def find_symbol_positions(string: str, symbol: str):
    positions = []
    for index, char in enumerate(string):
        if char == symbol:
            positions.append(index)
    return positions


def read_file(file_name: str) -> []:
    universe = []
    with open(file_name, "r") as file:
        row = 0
        for line in file:
            positions = find_symbol_positions(line, "#")
            for column in positions:
                universe.append(Galaxy(column, row))
            row += 1

    return universe


def manhattan_distance(galaxy1: Galaxy, galaxy2: Galaxy) -> int:
    return abs(galaxy1.x - galaxy2.x) + abs(galaxy1.y - galaxy2.y)


def day11_part1(file_name: str, size: int) -> int:
    # read the file & find the galaxies
    universe = read_file(file_name)

    # find the empty rows
    rows = [r for r in range(size)]
    for galaxy in universe:
        if galaxy.y in rows:
            rows.remove(galaxy.y)

    # find the empty columns
    columns = [c for c in range(size)]
    for galaxy in universe:
        if galaxy.x in columns:
            columns.remove(galaxy.x)

    for galaxy in universe:
        # update galaxies based on empty rows
        lesser_rows = [r for r in rows if r < galaxy.y]
        galaxy.y += len(lesser_rows)
        # update galaxies based on empty columns
        lesser_columns = [c for c in columns if c < galaxy.x]
        galaxy.x += len(lesser_columns)

    # find all the galaxy combinations
    total = 0
    for galaxy_idx in range(len(universe)):
        for galaxy_idx2 in range(galaxy_idx + 1, len(universe)):
            # for each combination, sum their manhattan distance
            total += manhattan_distance(universe[galaxy_idx], universe[galaxy_idx2])

    # and return the result
    return total


def test_day11_part1a() -> None:
    assert day11_part1("./input/day11a.txt", 10) == 374


def test_day11_part1b() -> None:
    assert day11_part1("./input/day11b.txt", 140) == 9418609

