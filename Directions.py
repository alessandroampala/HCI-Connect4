from enum import IntEnum


class Direction(IntEnum):
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
        if direction_generic == Direction.HORIZONTAL:
            return DirectionAccurate.E, DirectionAccurate.W
        if direction_generic == Direction.OBLIQUE_R:
            return DirectionAccurate.NE, DirectionAccurate.SW
        if direction_generic == Direction.OBLIQUE_L:
            return DirectionAccurate.NW, DirectionAccurate.SE


class DirectionAccurate(IntEnum):
    N = 0
    S = 1
    E = 2
    W = 3
    NE = 4
    NW = 5
    SE = 6
    SW = 7
