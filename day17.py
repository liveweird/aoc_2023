import unittest
from typing import List, Tuple
import abc

# enum with four directions
from enum import Enum
class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

class Position:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

class Plane(abc.ABC):
    @abc.abstractmethod
    def get_width(self) -> int:
        pass

    @abc.abstractmethod
    def get_height(self) -> int:
        pass

class Map(Plane):
    # map is a 2D array of digits
    def __init__(self, file_name: str):
        with open(file_name, "r") as file:
            self.map = [[int(c) for c in line.strip()] for line in file]

    def __str__(self):
        return "\n".join(["".join([str(c) for c in row]) for row in self.map])
    
    def get_width(self) -> int:
        return len(self.map[0])
    
    def get_height(self) -> int:
        return len(self.map)

class Graph(Plane):
    # graph is a 2D array of dictionaries
    def __init__(self, map: Map):
        self.map = map
        self.graph = [[{} for _ in range(map.get_width())] for _ in range(map.get_height())]
        self.queue = [Runner()]

    def are_we_done(self) -> bool:
        return len(self.queue) == 0
    
    def single_step(self) -> None:
        # pop the first runner of the queue
        runner = self.queue.pop(0)

        # get the possible moves
        moves = runner.get_possible_moves(self)

        # for each move ...
        for (move, traversal_cost) in moves:
            # calculate the total cost
            new_cost: int = traversal_cost + self.graph[runner.position.x][runner.position.y].get(runner.direction, 0)
            # if the cost in the graph is none or higher, update with new cost and add the runner to the queue
            compare_against: int = self.graph[move.position.x][move.position.y].get(move.direction, 999_999_999)
            if new_cost < compare_against:
                self.graph[move.position.x][move.position.y][move.direction] = new_cost
                self.queue.append(move)
            # if the cost is lower, do nothing
            else:
                pass

    def get_width(self) -> int:
        return len(self.graph[0])
    
    def get_height(self) -> int:
        return len(self.graph)

class Runner:
    def __init__(self, position: Position = Position(0, 0), direction: Direction = Direction.RIGHT) -> None:
        self.position: Position = position
        self.direction = direction

    def get_possible_moves(self, graph: Graph) -> List[Tuple['Runner', int]]:
        moves: List[Tuple['Runner', int]] = []
        traversal_cost: int = 0
        
        # get the three possible fields ahead
        for i in range(1, 4):
            new_pos: Position
            if self.direction == Direction.UP:
                new_pos = Position(self.position.x, self.position.y - i)
            elif self.direction == Direction.DOWN:
                new_pos = Position(self.position.x, self.position.y + i)
            elif self.direction == Direction.LEFT:
                new_pos = Position(self.position.x - i, self.position.y)
            elif self.direction == Direction.RIGHT:
                new_pos = Position(self.position.x + i, self.position.y)

            # if the field is not within the map, pass on it
            if new_pos.x < 0 or new_pos.x >= graph.get_width() or new_pos.y < 0 or new_pos.y >= graph.get_height():
                continue

            # for each of them add two possible moves, 90CW and 90CCW
            first_direction: Direction
            second_direction: Direction
            traversal_cost += graph.map.map[new_pos.x][new_pos.y]

            if self.direction == Direction.UP or self.direction == Direction.DOWN:
                first_direction = Direction.RIGHT
                second_direction = Direction.LEFT
            elif self.direction == Direction.LEFT or self.direction == Direction.RIGHT:
                first_direction = Direction.DOWN
                second_direction = Direction.UP

            moves.append((Runner(new_pos, first_direction), traversal_cost))
            moves.append((Runner(new_pos, second_direction), traversal_cost))

        # return the list of possible moves
        return moves

class Day17:
    @staticmethod
    def part1(file_name: str) -> int:
        result: int = 0

        map = Map(file_name)
        graph = Graph(map)
        while not graph.are_we_done():
            graph.single_step()

        return min(graph.graph[map.get_width() - 1][map.get_height() - 1].values())

    @staticmethod
    def part2(file_name: str) -> int:
        pass

class Tests(unittest.TestCase):
    def test_day17_part1a(self):
        self.assertEqual(Day17.part1("input/day17a.txt"), 102)

    def test_day17_part1b(self):
        self.assertEqual(Day17.part1("input/day17b.txt"), 698)
