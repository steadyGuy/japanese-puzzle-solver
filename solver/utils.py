"""Utility functions for the solver module."""
WHITE = 'W'
GREY = 'G'
BLACK = 'B'


class Region:
    """Region class to represent a region (room) in the grid."""

    def __init__(self, grid_inputs, symbol=''):
        self.grid_inputs = grid_inputs
        self.symbol = symbol

    def get_pos(self):
        """Get the coordinates of the region (room)."""
        return [(grid_input.x_pos, grid_input.y_pos) for grid_input in self.grid_inputs]

    def group_grid_inputs(self):
        """Group grid inputs based on their position."""
        cells = self.get_pos()
        for grid_input in self.grid_inputs:
            x, y = grid_input.get_pos()
            if (x - 1, y) not in cells:
                grid_input.west = True
            if (x, y + 1) not in cells:
                grid_input.south = True
            if (x + 1, y) not in cells:
                grid_input.east = True
            if (x, y - 1) not in cells:
                grid_input.north = True


class ValueInput:
    """ValueInput class to represent a cell in the grid."""

    def __init__(self, x_pos=None, y_pos=None, default_colour=None):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.symbol = ''
        self.default_colour = default_colour

        self.north = False
        self.east = False
        self.south = False
        self.west = False

    def get_pos(self):
        """Get the coordinates of the cell."""
        return self.x_pos, self.y_pos


def build_matrix(cords, x_matrix):
    """
    Builds a rectangular matrix based on a list of coordinates.

    Args:
        cords: A list of tuples representing (x, y) coordinates.
        x_matrix

    Returns:
        A 2D list representing the rectangular matrix.
    """

    # Find minimum and maximum x and y values
    min_x = min(coord[0] for coord in cords)
    max_x = max(coord[0] for coord in cords)
    min_y = min(coord[1] for coord in cords)
    max_y = max(coord[1] for coord in cords)

    # Create an empty matrix with appropriate dimensions
    rows = max_y - min_y + 1
    cols = max_x - min_x + 1
    matrix = [[0 for _ in range(cols)] for _ in range(rows)]

    # Fill the matrix with 1s at the corresponding coordinates
    for x, y in cords:
        matrix[y - min_y][x - min_x] = x_matrix[x, y, 1]

    return matrix


class InvalidInputError(Exception):
    """InvalidInputError class to handle invalid input errors."""
