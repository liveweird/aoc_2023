import numpy as np
import typing
from math import ceil, floor
from typing import Callable


# define a class for a race, that has two properties: the record and the time
class Race:
    def __init__(self, time: int, record: str):
        self.time = time
        self.record = record


def get_races_a() -> list:
    races: list = [Race(7, 9), Race(15, 40), Race(30, 200)]
    return races


def get_races_b() -> list:
    races: list = [Race(40, 215), Race(92, 1064), Race(97, 1505), Race(90, 1100)]
    return races


def get_races_c() -> list:
    races: list = [Race(71530, 940200)]
    return races


def get_races_d() -> list:
    races: list = [Race(40929790, 215106415051100)]
    return races


def day06_part1(get_races: Callable[[], list]) -> int:
    # get races
    races: list = get_races()
    result: int = 1

    # get through each race
    for race in races:
        # find the roots
        coeffs = [-1, race.time, -1 * race.record]
        roots: list = np.roots(coeffs)
        roots.sort()
        spread = ceil(roots[1] - 1) - floor(roots[0] + 1) + 1

        result *= spread

    return result


def test_day06_part1a():
    assert day06_part1(get_races_a) == 288


def test_day06_part1b():
    assert day06_part1(get_races_b) == 6209190


def test_day06_part2a():
    assert day06_part1(get_races_c) == 71503


def test_day06_part2b():
    assert day06_part1(get_races_d) == 28545089
