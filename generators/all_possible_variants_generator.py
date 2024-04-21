"""Module to generate all possible variants of a matrix to solve"""
import copy
import itertools

from solver.solver import Solver
from database import DB


def generate_all_variants_of_a_room(rooms, keys):
    """Generate all possible variants of a room with S, A or empty string"""
    variants = []
    for variant in itertools.product(keys, repeat=len(rooms)):
        for i, room in enumerate(rooms):
            first_key = next(iter(room))
            room[first_key] = variant[i]
        variants.append(copy.deepcopy(rooms))

    return variants


def dfs(matrix, visited, row, col, group, num):
    """Depth-first search to traverse the matrix and identify the connected components"""
    if (
        row < 0
        or col < 0
        or row >= len(matrix)
        or col >= len(matrix[0])
        or matrix[row][col] == num
        or visited[row][col]
    ):
        return

    visited[row][col] = True
    group[f'{row},{col}'] = ''

    dfs(matrix, visited, row + 1, col, group, num)  # Explore down
    dfs(matrix, visited, row - 1, col, group, num)  # Explore up
    dfs(matrix, visited, row, col + 1, group, num)  # Explore right
    dfs(matrix, visited, row, col - 1, group, num)  # Explore left


def group_connected_components(matrix, num=1):
    """Convert a matrix of 1/0 to a list of rooms/regions with coordinates"""
    rows, cols = len(matrix), len(matrix[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    groups = []

    for i in range(rows):
        for j in range(cols):
            if matrix[i][j] == num and not visited[i][j]:
                group = {}
                dfs(matrix, visited, i, j, group, 0 if num == 1 else 1)
                groups.append(group)

    return groups


async def generate_variants(matrix_size, client_symbols=None, start=None, end=None):
    """Generate all possible variants of a matrix based on the matrix size 
    and symbols provided by the client"""

    if client_symbols is None:
        client_symbols = []

    symbols = [""]
    symbols.extend(client_symbols)

    possible_variants_count = 0

    row_variants = list(itertools.product([0, 1], repeat=matrix_size))
    num_variants = len(row_variants)

    if start is None:
        start = 0

    if end is None:
        end = num_variants ** matrix_size

    collection = DB[f'variant-{matrix_size}']

    # empty the collection before inserting new data
    await collection.delete_many({})

    for i in range(min(start, end), min(num_variants ** matrix_size, end)):
        matrix = []
        for j in range(matrix_size):
            row_idx = (i // (num_variants ** j)) % num_variants
            matrix.append(row_variants[row_idx])

        rooms_part_1, rooms_part_0 = group_connected_components(
            matrix, 1), group_connected_components(
            matrix, 0)

        condition = rooms_part_1 + rooms_part_0

        conditions = generate_all_variants_of_a_room(condition, symbols)
        for room in conditions:
            solver = Solver(room)
            solution = solver.solve()
            if len(solution) != 0:
                _ = collection.insert_one(
                    {"condition": condition, "solution": solution})
                possible_variants_count += 1

    return possible_variants_count
