from typing import List

from classes.Point import Point


class Sector:
    def __init__(self, max: int, min: int, points: List[Point]):
        self.max = max
        self.min = min
        self.points = points
