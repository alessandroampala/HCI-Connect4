from enum import Enum, auto


class Direction(Enum):
    HORIZONTAL = 0
    VERTICAL = 1
    OBLIQUE_R = 2  # Represents NE && SW direction
    OBLIQUE_L = 3  # Represents NW && SE direction

    @staticmethod
    def accurate_to_generic(direction_accurate):
        if direction_accurate == DirectionAccurate.N or direction_accurate == DirectionAccurate.S:
            return Direction.VERTICAL
        if direction_accurate == DirectionAccurate.E or direction_accurate == DirectionAccurate.W:
            return Direction.HORIZONTAL
        if direction_accurate == DirectionAccurate.NE or direction_accurate == DirectionAccurate.SW:
            return Direction.OBLIQUE_R
        if direction_accurate == DirectionAccurate.NW or direction_accurate == DirectionAccurate.SE:
            return Direction.OBLIQUE_L

    @staticmethod
    def generic_to_accurate(direction_generic):
        if direction_generic == Direction.VERTICAL:
            return DirectionAccurate.N, DirectionAccurate.S
        if direction_generic == Direction.VERTICAL:
            return DirectionAccurate.E, DirectionAccurate.E
        if direction_generic == Direction.OBLIQUE_R:
            return DirectionAccurate.NE, DirectionAccurate.SW
        if direction_generic == Direction.OBLIQUE_L:
            return DirectionAccurate.NW, DirectionAccurate.SE


class DirectionAccurate(Enum):
    N = 0
    S = auto()
    E = auto()
    W = auto()
    NE = auto()
    NW = auto()
    SE = auto()
    SW = auto()
