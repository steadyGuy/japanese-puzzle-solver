"""Rooms generator module."""
import random

from gurobipy.gurobipy import GurobiError

from solver.solver import Solver
from solver.utils import InvalidInputError


def generate_cords_from_number(grid_size):
    """Generate coordinates from a number."""
    coordinates = {}
    for i in range(grid_size):
        for j in range(grid_size):
            coordinates[f'{j},{i}'] = None
    return coordinates


def generate_room(length_limit):
    """Generate a room length and symbol."""
    room_length = random.randint(1, length_limit)
    room_symbols = ['', 'S', 'A']
    room_symbol = random.choice(room_symbols)
    return room_length, room_symbol


def generate_rooms(size):
    """Generate rooms."""
    if size <= 1 or size >= 23:
        raise InvalidInputError(
            "The amount of rows and columns must be between 2 and 23")

    cords_list = generate_cords_from_number(size)

    x, y = [random.randint(0, size - 1), random.randint(0, size - 1)]
    k = 1
    obj = {}
    result = []
    while len(cords_list) > 0:
        step = random.randint(1, size)
        room_length, room_symbol = generate_room(len(cords_list))
        while room_length != 0:
            try:
                for i in range(step):
                    if room_length == 0:
                        break
                    if (x + i) == size:
                        break
                    del cords_list[f'{i + x},{y}']
                    obj[f"{y},{i + x}"] = ""
                    room_length -= 1

                # we are on the lower bound
                y += 1
                if y == size:
                    # then go to the upper bound
                    y = 0
                    # new room
                    break
            except KeyError:
                break

        # take next cell
        if len(cords_list) > 0:
            data = next(iter(cords_list)).split(',')
            x, y = int(data[0]), int(data[1])
        k += 1
        random_key = random.choice(list(obj.keys()))
        obj[random_key] = room_symbol
        result.append(obj)
        obj = {}

    try:
        solver = Solver(result)
        solution = solver.solve()
        if len(solution) < 1:
            result = generate_rooms(size)
    except GurobiError:
        return result

    return result
