"""Tests for the `generate_rooms` function in `solver/rooms_generator.py`."""
import random
import pytest

from generators.generate_randomly import generate_rooms
from solver.utils import InvalidInputError


def test_generate_rooms_valid_input():
    """Test for valid input."""
    # Define a fixed random seed for predictable results
    random.seed(0)

    size = 10
    result = generate_rooms(size)
    print(len(result))
    assert isinstance(result, list)
    assert len(result) == 11


def test_generate_rooms_invalid_input():
    """Test for invalid input."""
    with pytest.raises(InvalidInputError) as exc_info:
        size = 1  # Size less than 2
        generate_rooms(size)
    assert str(
        exc_info.value) == "The amount of rows and columns must be between 2 and 23"

    with pytest.raises(InvalidInputError) as exc_info:
        size = 30  # Size greater than 26
        generate_rooms(size)
    assert str(
        exc_info.value) == "The amount of rows and columns must be between 2 and 23"


def test_generate_rooms_output():
    """Test the output of the `generate_rooms` function."""
    # Define a fixed random seed for predictable results
    random.seed(0)

    size = 8
    result = generate_rooms(size)
    assert isinstance(result, list)
    # assert len(result) == size

    # Assuming each room is represented as a dictionary with keys as coordinates
    # and values as room symbols
    for room in result:
        assert isinstance(room, dict)
        assert all(isinstance(key, str) and len(
            key.split(',')) == 2 for key in room.keys())
        assert all(symbol in {'', 'S', 'A'} for symbol in room.values())

    # Additional assertions can be added based on the specific behavior of the function
