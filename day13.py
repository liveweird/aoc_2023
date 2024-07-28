class Picture:
    def __init__(self):
        self.sequences = []
        self.is_pivoted = False
        self.pivoted = []

    def add_sequence(self, sequence: str) -> None:
        self.sequences.append(sequence)

    def pivot(self) -> None:
        self.is_pivoted = True
        self.pivoted = ["".join(column) for column in zip(*self.sequences)]

    def __str__(self) -> str:
        return "\n".join(self.pivoted)


def read_pictures(file_name: str) -> list[Picture]:
    pictures = []
    picture = Picture()
    # read the file, retrieve the list of pictures
    with open(file_name) as file:
        for line in file:
            if line == "\n":
                picture.pivot()
                pictures.append(picture)
                picture = Picture()
            else:
                picture.add_sequence(line.strip())
        picture.pivot()
        pictures.append(picture)

    return pictures


def find_mirrors_edge(sequences: list[str]) -> int:
    results = []
    # iterate through all the sequences but the last one
    for i in range(len(sequences) - 1):
        # if this sequence is exactly the same as the next one
        left = i
        right = i + 1
        saved_left = left
        while True:
            if left < 0 or right >= len(sequences):
                results.append(saved_left)
                break
            if sequences[left] == sequences[right]:
                # print(f"It's a match: {left}")
                left = left - 1
                right = right + 1
            else:
                break

    return results


def day13_part1(file_name: str) -> int:
    result = 0

    pictures = read_pictures(file_name)
    for picture in pictures:
        rows = find_mirrors_edge(picture.sequences)
        # print(f"Rows: {rows}")
        for row in rows:
            result += 100 * (row + 1)
        columns = find_mirrors_edge(picture.pivoted)
        # print(f"Columns: {columns}")
        for column in columns:
            result += (column + 1)

    return result


def test_day13_part1a() -> None:
    assert day13_part1("./input/day13a.txt") == 405


def test_day13_part1b() -> None:
    assert day13_part1("./input/day13b.txt") == 405