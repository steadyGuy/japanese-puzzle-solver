"""Solver class for this task"""

from typing import Any

from gurobipy.gurobipy import Model
from gurobipy import GRB, quicksum

from solver.utils import ValueInput, build_matrix, Region, WHITE, GREY, BLACK, InvalidInputError


class Solver:
    """Solver class"""

    def __init__(self, input_matrix=None):
        if input_matrix is None:
            input_matrix = []
        self.boundary_cells = 0
        self.loop_found = None
        self.visited_black_cells = []
        self.visited_cells = []

        ##################################
        self.lazy_constraints_added = 0
        self.grid_inputs: dict[Any, Any] = {}  # Dictionary of inp objects
        self.length = 0  # Grid dimension

        self.regions = []  # List of Region objects
        self.init_regions(input_matrix)

    def cell_neigh(self, cell):
        """Return a list of neighbouring cells"""
        neighbours = []
        i, j = cell
        if i > 0:
            neighbours.append((i - 1, j))
        if j < self.length - 1:
            neighbours.append((i, j + 1))
        if i < self.length - 1:
            neighbours.append((i + 1, j))
        if j > 0:
            neighbours.append((i, j - 1))
        return neighbours

    def vert_neigh(self, cell):
        """Return a list of vertically connected cells"""
        neighbours = []
        regions = []
        for i in range(cell[1], self.length):
            neighbours.append((cell[0], i))
            for region in self.regions:
                if (cell[0], i) in region.get_pos():
                    if region not in regions:
                        regions.append(region)
                    if len(regions) >= 3:
                        return neighbours
        return False

    # Iterate east until a string of cells has been collected that spans exactly 3 regions.
    # Otherwise, return False
    def hor_neigh(self, cell):
        """Return a list of horizontally connected cells"""
        neighbours = []
        regions = []
        for i in range(cell[0], self.length):
            neighbours.append((i, cell[1]))
            for region in self.regions:
                if (i, cell[1]) in region.get_pos():
                    if region not in regions:
                        regions.append(region)
                    if len(regions) >= 3:
                        return neighbours
        return False

    def diagonal_neighbours(self, cell):
        """Return a list of diagonally connected cells"""
        neighbours = []
        i, j = cell
        if i - 1 >= 0 and j - 1 >= 0:
            neighbours.append((i - 1, j - 1))
        if i - 1 >= 0 and j + 1 <= self.length - 1:
            neighbours.append((i - 1, j + 1))
        if i + 1 <= self.length - 1 and j + 1 <= self.length - 1:
            neighbours.append((i + 1, j + 1))
        if i + 1 <= self.length - 1 and j - 1 >= 0:
            neighbours.append((i + 1, j - 1))
        return neighbours

    def follow_black_cells_loop(self, prev_cell, cell, xv):
        """Follow black cells to find a loop"""
        if cell in self.visited_cells:
            return
        self.visited_cells.append(cell)
        self.visited_black_cells.append(cell)
        for (i, j) in self.diagonal_neighbours(cell):
            if xv[(i, j, 1)] > 0.9:  # if the neighbouring cell is black
                # If the neighbouring cell is NOT the previous cell, but it has been visited,
                # then we have found a loop
                if (i, j) != prev_cell and (i, j) in self.visited_cells:
                    self.loop_found = True
                    return
                if not self.loop_found:
                    self.follow_black_cells_loop(cell, (i, j), xv)

    # Iterate through all diagonally connected black cells.
    # If two distinct boundary points have been found,
    # then an impenetrable black wall has been found.
    def follow_black_cells(self, cell, xv):
        """Follow black cells to find a wall"""
        if cell in self.visited_cells:
            return
        if (cell[0] == 0 or cell[0] == self.length - 1 or cell[1] == 0
                or cell[1] == self.length - 1):  # If cell on boundary
            self.boundary_cells += 1
        self.visited_cells.append(cell)
        self.visited_black_cells.append(cell)
        if self.boundary_cells > 1:
            return
        for (i, j) in self.diagonal_neighbours(cell):
            if xv[(i, j, 1)] > 0.9:
                self.follow_black_cells((i, j), xv)

    def purge_trails(self, loop_mode):
        """Purge trailing points"""
        trail_exists = True
        while trail_exists:
            trail_exists = False
            for cell in self.visited_cells:
                if not loop_mode:
                    # If on boundary, don't count as endpoint
                    if (cell[0] == 0 or cell[0] == self.length - 1 or
                            cell[1] == 0 or cell[1] == self.length - 1):
                        continue
                neighbours = self.diagonal_neighbours(cell)
                if len(set(self.visited_cells).intersection(neighbours)) == 1:  # Found an endpoint
                    trail_exists = True
                    self.visited_cells.remove(cell)

    def init_regions(self, regions):
        """Initialize regions"""
        max_x, max_y = [0, 0]
        missing_coordinates = []
        all_keys = set()

        # Accumulate all keys
        for grid_dict in regions:
            all_keys.update(grid_dict.keys())

        # Calculate max_x and max_y
        for coord in all_keys:
            x, y = map(int, coord.split(','))
            max_x = max(max_x, x)
            max_y = max(max_y, y)

        if max_x != max_y:
            raise InvalidInputError(
                "The amount of rows and columns of the matrix are not equal")
        # too big number would make the model too complex for
        # gurobi to solve in free version
        if max_x < 4 or max_x >= 23:
            raise InvalidInputError(
                "The amount of rows and columns must be between 5 and 23")

        # Check for missing coordinates
        for x in range(max_x):
            for y in range(max_y):
                if f"{x},{y}" not in all_keys:
                    missing_coordinates.append((x, y))

        if len(missing_coordinates) > 0:
            raise InvalidInputError(
                "Some regions are not filled", missing_coordinates)

        self.length = max_x + 1
        for region in regions:
            region_symbol = ''
            grid_inputs = []
            for coord, symbol in region.items():
                i, j = map(int, coord.split(','))
                if symbol not in ('', 'S', 'A'):
                    raise ValueError(
                        "Invalid value in coordinates, must be empty string or 'S'/'A'.")

                grid_input_obj = ValueInput(i, j, GREY)
                self.grid_inputs[(i, j)] = grid_input_obj
                grid_inputs.append(grid_input_obj)
                if symbol:
                    grid_input_obj.symbol = symbol
                    region_symbol = symbol
            region_obj = Region(grid_inputs, region_symbol)
            self.regions.append(region_obj)
            region_obj.group_grid_inputs()

    def solve(self):
        """Matrix solver"""
        self.lazy_constraints_added = 0
        for inp in self.grid_inputs.values():
            inp.default_colour = GREY

        m = Model("Solver")
        x = {
            (i, j, col): m.addVar(vtype=GRB.BINARY, obj=0, ub=1, lb=0, name="var", column=None)
            for (i, j), _ in self.grid_inputs.items() for col in
            [0, 1]
        }

        # select one constraint
        for (i, j), _ in self.grid_inputs.items():
            [black_1, white_1] = [x[i, j, 0], x[i, j, 1]]
            one_constraint = black_1 + white_1 == 1
            m.addConstr(one_constraint, name='one constraint')

        # region symbol
        for region in self.regions:
            if region.symbol:
                cells = region.get_pos()
                matrix = build_matrix(cells, x)
                m_reversed = [row[::-1] for row in reversed(matrix)]

                if region.symbol == 'S':
                    for i, _ in enumerate(matrix):
                        for j, _ in enumerate(matrix[0]):
                            [v1, v2] = [matrix[i][j], m_reversed[i][j]]
                            constraint: Any = v1 == v2
                            m.addConstr(constraint,
                                        name='compare_' + str(i) + '_' + str(j))

                if region.symbol == 'A':
                    for i, _ in enumerate(matrix):
                        for j, _ in enumerate(matrix[0]):
                            [v1, v2] = [matrix[i][j], m_reversed[i][j]]
                            constraint = v1 + v2 <= 1
                            m.addConstr(
                                constraint, name='not_equal_' + str(i) + '_' + str(j))

        # AdjacentBlack
        _ = [m.addConstr(
            quicksum(x[ii, jj, 1] for (ii, jj) in self.cell_neigh(
                (i, j))) <= len(self.cell_neigh((i, j))) * (1 - x[i, j, 1]))
             for (i, j), _ in self.grid_inputs.items()]

        vert_orthogonal = {}
        for (i, j), inp in self.grid_inputs.items():
            if inp.south:
                neighbours = self.vert_neigh(inp.get_pos())
                if neighbours:
                    vert_orthogonal[(i, j)] = m.addConstr(
                        quicksum(x[ii, jj, 1]
                                 for (ii, jj) in neighbours) >= 1)

        hor_orthogonal = {}
        for (i, j), inp in self.grid_inputs.items():
            if inp.east:
                neighbours = self.hor_neigh(inp.get_pos())
                if neighbours:
                    hor_orthogonal[(i, j)] = m.addConstr(
                        quicksum(x[ii, jj, 1]
                                 for (ii, jj) in neighbours) >= 1)

        # ConnectedAtLeast
        _ = [
            m.addConstr(quicksum(x[ii, jj, 0] for (
                ii, jj) in self.cell_neigh((i, j))) >= x[i, j, 0])
            for (i, j), _ in self.grid_inputs.items()]

        def callback(model, where):
            if where == GRB.callback.MIPSOL:

                xv = {k: v for (k, v) in zip(
                    x.keys(), model.cbGetSolution(list(x.values())))}

                # upd current solution in grid_inputs
                for (i, j), grid_input_new in self.grid_inputs.items():
                    if xv[(i, j, 1)] > 0.9:
                        grid_input_new.default_colour = BLACK
                    else:
                        grid_input_new.default_colour = WHITE

                self.visited_black_cells = []
                for k in xv:
                    # If cell on boundary
                    if k[0] in [0, self.length - 1] or k[1] in [0, self.length - 1]:
                        # If cell is black and hasn't been checked yet
                        if (xv[(k[0], k[1], 1)] > 0.9 and (k[0], k[1])
                                not in self.visited_black_cells):
                            self.boundary_cells = 0
                            self.visited_cells = []
                            self.follow_black_cells((k[0], k[1]), xv)
                            if self.boundary_cells > 1:
                                # PURGE TRAILING POINTS:
                                self.purge_trails(loop_mode=False)

                                self.lazy_constraints_added += 1
                                model.cbLazy(quicksum(x[(i, j, 1)] for (
                                    i, j) in self.visited_cells) <= len(self.visited_cells) - 1)
                                break

                self.visited_black_cells = []
                for k in xv:
                    # If cell is black and hasn't been checked yet
                    if xv[(k[0], k[1], 1)] > 0.9 and (k[0], k[1]) not in self.visited_black_cells:
                        self.loop_found = False
                        self.visited_cells = []
                        self.follow_black_cells_loop(0, (k[0], k[1]), xv)
                        if self.loop_found:
                            # PURGE TRAILING POINTS:
                            self.purge_trails(loop_mode=True)

                            self.lazy_constraints_added += 1
                            model.cbLazy(quicksum(x[(i, j, 1)] for (
                                i, j) in self.visited_cells) <= len(self.visited_cells) - 1)
                            break

        m.setParam('LazyConstraints', 1)
        m.optimize(callback)
        if m.status != 2:
            return []

        return self.get_result()

    def get_result(self):
        """Get the result"""
        # Create an empty list to store the rows
        matrix = []

        # Loop self.length times to create self.length rows
        for _ in range(self.length):
            # Create an empty list for each row
            row = []
            for _ in range(self.length):
                row.append(0)  # Add 0 to each element in the row
            # Add the completed row to the matrix
            matrix.append(row)

        for inp in self.grid_inputs.values():
            matrix[inp.y_pos][inp.x_pos] = inp.default_colour
            if inp.symbol:
                matrix[inp.y_pos][inp.x_pos] += f"/{inp.symbol}"
        return matrix
