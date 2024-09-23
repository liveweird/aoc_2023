import re, unittest
from abc import abstractmethod
from typing import List

class Command:
    def __init__(self, label: str):
        self.label = label

    @property
    def labels_hash(self):
        return Day15.calc_hash(self.label)

    @abstractmethod
    def process(self, blocks: dict) -> dict:
        pass

class CommandSet(Command):
    def __init__(self, label: str, focal: int):
        super().__init__(label)
        self.focal = focal

    def process(self, blocks: dict) -> dict:
        # get the block with the index equal to labels_hash
        block = blocks.get(self.labels_hash, [])

        # if the block contains an entry with label equal to self.label, update the focal value
        for entry in block:
            if entry["label"] == self.label:
                entry["focal"] = self.focal
                break
        else:
            # if the block does not contain an entry with label equal to self.label, add a new entry
            block.append({"label": self.label, "focal": self.focal})

        # update the block in the blocks dictionary
        blocks[self.labels_hash] = block

        return blocks


class CommandDel(Command):
    def __init__(self, label: str):
        super().__init__(label)

    def process(self, blocks: dict) -> dict:
        # get the block with the index equal to labels_hash
        block = blocks.get(self.labels_hash, [])

        # remove the entry with label equal to self.label
        block = [entry for entry in block if entry["label"] != self.label]

        # update the block in the blocks dictionary
        blocks[self.labels_hash] = block

        return blocks


class Day15:
    @staticmethod
    def calc_hash(sequence: str) -> int:
        result = 0
        # for every character in the sequence ...
        for char in sequence:
            # get the ASCII code of the char
            ascii_code = ord(char)
            result += ascii_code
            result *= 17
            # get the remainder of the division by 256
            result %= 256

        return result

    @staticmethod
    def parse_command(serialized: str) -> Command:
        regex = r"([a-zA-Z]+)(=\d)?(-)?"
        match = re.match(regex, serialized)
        label = match.group(1)
        focal = match.group(2)
        if focal is not None:
            return CommandSet(label, int(focal[1:]))
        else:
            return CommandDel(label)

    @staticmethod
    def parse_commands(sequences: List[str]) -> List[Command]:
        commands = []
        for sequence in sequences:
            commands.append(Day15.parse_command(sequence))
        return commands

    @staticmethod
    def summarize_blocks(blocks: dict) -> int:
        result = 0
        for key, value in blocks.items():
            for idx, entry in enumerate(value):
                result += (key + 1) * (idx + 1) * entry["focal"]
        return result

    def part1(self, file_name: str) -> int:
        result = 0
        # open the file_name file & read the single line
        with open(file_name, "r") as file:
            line = file.readline().strip()

            # split the line by commas
            sequences: list[str] = list(line.split(","))

            # for every sequence, calculate the hash
            for sequence in sequences:
                hashed = self.calc_hash(sequence)

                # sum all the hashes & return them
                result += hashed

        return result

    def part2(self, file_name: str) -> int:
        blocks = {}
        # open the file_name file & read the single line
        with open(file_name, "r") as file:
            line = file.readline().strip()

            # split the line by commas
            sequences: list[str] = list(line.split(","))
            commands = self.parse_commands(sequences)

            for command in commands:
                blocks = command.process(blocks)

        result = self.summarize_blocks(blocks)
        return result


class Tests(unittest.TestCase):
    def test_day15_part1a(self):
        self.assertEqual(Day15().part1("./input/day15a.txt"), 52)

    def test_day15_part1b(self):
        self.assertEqual(Day15().part1("./input/day15b.txt"), 1320)

    def test_day15_part1c(self):
        self.assertEqual(Day15().part1("./input/day15c.txt"), 510013)

    def test_day15_create_command_set(self):
        command = Day15.parse_command("abc=3")
        self.assertIsInstance(command, CommandSet)
        self.assertEqual(command.label, "abc")
        self.assertEqual(command.focal, 3)

    def test_day15_create_command_del(self):
        command = Day15.parse_command("abc")
        self.assertIsInstance(command, CommandDel)
        self.assertEqual(command.label, "abc")

    def test_day15_part2a(self):
        self.assertEqual(Day15().part2("./input/day15b.txt"), 145)

    def test_day15_part2b(self):
        self.assertEqual(Day15().part2("./input/day15c.txt"), 268497)

if __name__ == '__main__':
    unittest.main()