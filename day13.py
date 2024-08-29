import unittest

class Line(str):
    def __init__(self, line: str):
        self.line = line

    def __str__(self):
        return self.line

    def diffs(self, other):
        diffs = sum(c1 != c2 for c1, c2 in zip(self.line, other.line))
        return diffs

class Picture:
    def __init__(self):
        self.sequences = []
        self.is_pivoted = False
        self.pivoted = []

    def add_sequence(self, sequence: str) -> None:
        self.sequences.append(Line(sequence))

    def pivot(self) -> None:
        self.is_pivoted = True
        strings_pivoted = ["".join(column) for column in zip(*self.sequences)]
        self.pivoted = [Line(string_pivoted) for string_pivoted in strings_pivoted]

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


def find_mirrors_edge(sequences: list[str]) -> list[int]:
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
            if sequences[left].line == sequences[right].line:
                # print(f"It's a match: {left}")
                left = left - 1
                right = right + 1
            else:
                break

    return results


def find_imperfect_mirrors_edge(sequences: list[str]) -> list[int]:
    results = []
    # iterate through all the sequences but the last one
    for i in range(len(sequences) - 1):
        # set up the total sum of differences
        total_diffs = 0
        allowed_diffs = 1
        # if the error is in accepted range
        left = i
        right = i + 1
        saved_left = left
        while True:
            if (left < 0 or right >= len(sequences)):
                if (total_diffs == allowed_diffs):
                    results.append(saved_left)
                break
            calced_diffs = sequences[left].diffs(sequences[right])
            if (total_diffs + calced_diffs) <= allowed_diffs:
                total_diffs += calced_diffs
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
        for row in rows:
            result += 100 * (row + 1)
        columns = find_mirrors_edge(picture.pivoted)
        for column in columns:
            result += (column + 1)

    return result


def day13_part2(file_name: str) -> int:
    result = 0

    pictures = read_pictures(file_name)
    for picture in pictures:
        rows = find_imperfect_mirrors_edge(picture.sequences)
        # print(f"Rows: {rows}")
        for row in rows:
            result += 100 * (row + 1)
        columns = find_imperfect_mirrors_edge(picture.pivoted)
        # print(f"Columns: {columns}")
        for column in columns:
            result += (column + 1)

    return result


class Tests(unittest.TestCase):
    def test_day13_part1a(self) -> None:
        self.assertEqual(day13_part1("./input/day13a.txt"), 405)


    def test_day13_part1b(self) -> None:
        self.assertEqual(day13_part1("./input/day13b.txt"), 41859)


    def test_day13_part2a(self) -> None:
        self.assertEqual(day13_part2("./input/day13a.txt"), 400)


    def test_day13_part2b(self) -> None:
        self.assertEqual(day13_part2("./input/day13b.txt"), 30842)


if __name__ == "__main__":
    unittest.main()
