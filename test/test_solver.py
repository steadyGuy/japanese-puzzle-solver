"""Test the solver module"""
import pytest
import numpy as np

from solver.solver import Solver
from solver.utils import InvalidInputError

matrix_10x10_real_solution = np.array(
    [['W', 'W', 'W', 'W', 'W', 'B', 'W', 'B', 'W', 'W'],
     ['W', 'B', 'W', 'W/A', 'B', 'W', 'W', 'W', 'W', 'B/A'],
     ['W', 'W', 'B', 'W', 'W/A', 'W', 'W', 'B', 'W', 'W'],
     ['B', 'W', 'W', 'B', 'W', 'B', 'W', 'W/A', 'B/A', 'W'],
     ['W', 'W', 'B', 'W', 'W', 'W', 'B', 'W', 'W', 'B/S'],
     ['W/S', 'B', 'W', 'W', 'B', 'W', 'W', 'B', 'W', 'W'],
     ['B', 'W/A', 'W/S', 'W', 'W', 'B', 'W', 'W', 'B', 'W'],
     ['W', 'W', 'B', 'W', 'W', 'W/A', 'B', 'W', 'W', 'B'],
     ['W/A', 'B', 'W', 'W', 'B', 'W', 'W/S', 'B', 'W', 'W'],
     ['B', 'W', 'W', 'W', 'W', 'B', 'W', 'W', 'B', 'W']]
)

matrix_7x7_real_solution = np.array(
    [['W', 'B/S', 'W', 'W/A', 'W', 'W', 'W'],
     ['W', 'W', 'B', 'W', 'B', 'W', 'B'],
     ['B', 'W/S', 'W', 'B/A', 'W', 'W', 'W'],
     ['W', 'B/A', 'W', 'W/S', 'W', 'B', 'W'],
     ['W', 'W', 'W', 'B', 'W', 'W', 'W'],
     ['W/S', 'W', 'B', 'W', 'W', 'W', 'B'],
     ['B', 'W', 'W', 'W', 'B', 'W', 'W']]
)


# can't resolve warning because of pytest fixture
def test_solution_matrix_10x10(solution_10x10):
    """
    Validate the solution for 10x10 matrix
    """
    _solution_10x10 = np.array(solution_10x10.solve())
    assert np.array_equal(matrix_10x10_real_solution, _solution_10x10)


# can't resolve warning because of pytest fixture
def test_solution_matrix_7x7(solution_7x7):
    """
    Validate the solution for 7x7 matrix
    """
    _solution_7x7 = np.array(solution_7x7.solve())
    assert np.array_equal(matrix_7x7_real_solution, _solution_7x7)


too_small_input = [
    {'0,0': ''},
]


def test_solution_too_small():
    """Test that raises InvalidInputError if input values are small"""
    with pytest.raises(InvalidInputError) as exc_info:
        Solver(input_matrix=too_small_input)
    assert str(
        exc_info.value) == "The amount of rows and columns must be between 2 and 23"


too_big_input = [
    {'0,36': '', '36,0': '', }
]


def test_solution_too_big():
    """Test that raises InvalidInputError if input values are big"""
    with pytest.raises(InvalidInputError) as exc_info:
        Solver(input_matrix=too_big_input)
    assert str(
        exc_info.value) == "The amount of rows and columns must be between 2 and 23"


different_rows_and_cols = [
    {'0,0': '', '0,1': 'S'},
    {'1,0': '', '2,1': '', '2,0': ''},
]


def test_solution_different_amount_of_rows_and_columns():
    """Test that raises InvalidInputError if
    the amount of rows and columns of the matrix are not equal"""
    with pytest.raises(InvalidInputError) as exc_info:
        Solver(input_matrix=different_rows_and_cols)
    assert str(
        exc_info.value) == "The amount of rows and columns of the matrix are not equal"


input_matrix_7x7_without_0_0 = [{'1,0': 'S', '2,0': '', '1,1': '', '2,1': '', '3,1': ''},
                                {'3,0': 'A', '4,0': '', '5,0': '', '6,0': '',
                                    '6,1': '', '5,1': '', '4,1': ''},
                                {'0,1': ''}, {'0,2': ''},
                                {'1,2': 'S', '2,2': ''}, {'3,2': 'A',
                                                          '4,2': '', '5,2': '', '6,2': ''},
                                {'0,3': '', '0,4': ''},
                                {'1,3': 'A', '2,3': '', '1,4': '', '2,4': ''},
                                {'3,3': 'S', '4,3': '', '5,3': '', '6,3': '', '3,4': '',
                                 '4,4': '', '5,4': '',
                                 '6,4': '', '3,5': '', '4,5': '',
                                 '5,5': '', '6,5': '', '3,6': '', '4,6': '', '5,6': '', '6,6': ''},
                                {'0,5': 'S', '1,5': '', '2,5': '', '0,6': '', '1,6': '', '2,6': ''}]


def test_solution_missing_coordinates():
    """Test that raises InvalidInputError if
    some regions are not filled"""
    with pytest.raises(InvalidInputError) as exc_info:
        Solver(input_matrix=input_matrix_7x7_without_0_0)
    assert str(exc_info.value) == "('Some regions are not filled', [(0, 0)])"

    missing_coordinates = exc_info.value.args[1]
    assert missing_coordinates == [(0, 0)]


def test_check_input_validity():
    """Test that raises InvalidInputError if
    invalid value in coordinates were provided"""

    inp_test = [{'0,0': 'X', '1,0': 'X', '2,0': 'X', '1,1': 'X', '2,1': 'X', '3,1': 'X'},
                {'3,0': 'A', '4,0': '', '5,0': '', '6,0': '',
                    '6,1': '', '5,1': '', '4,1': ''}, {'0,1': ''},
                {'0,2': ''}, {'1,2': 'S', '2,2': ''}, {
                    '3,2': 'A', '4,2': '', '5,2': '', '6,2': ''},
                {'0,3': '', '0,4': ''}, {'1,3': 'A',
                                         '2,3': '', '1,4': '', '2,4': ''},
                {'3,3': 'S', '4,3': '', '5,3': '', '6,3': '', '3,4': '', '4,4': '',
                 '5,4': '', '6,4': '', '3,5': '',
                 '4,5': '', '5,5': '', '6,5': '', '3,6': '', '4,6': '', '5,6': '', '6,6': ''},
                {'0,5': 'S', '1,5': '', '2,5': '', '0,6': '', '1,6': '', '2,6': ''}]

    with pytest.raises(ValueError) as exc_info:
        Solver(input_matrix=inp_test)
    assert str(
        exc_info.value) == "Invalid value in coordinates, must be empty string or 'S'/'A'."
