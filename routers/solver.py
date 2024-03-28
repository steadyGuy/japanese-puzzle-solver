"""Endpoints for the solver module."""
from typing import List, Dict
from test.test_solver import input_matrix_7x7
from fastapi import APIRouter, HTTPException
from gurobipy import GurobiError
from pydantic import BaseModel

from solver.rooms_generator import generate_rooms
from solver.solver import Solver
from solver.utils import InvalidInputError

router = APIRouter(
    prefix='/api',
    tags=['solver']
)

example_data_for_docs: list = [
    {
        "coordinates": input_matrix_7x7
    }
]


class InputData(BaseModel):
    """Input data for the solver endpoint"""
    coordinates: List[Dict[str, str]]

    model_config = {
        "json_schema_extra": {
            "examples": example_data_for_docs,
        }
    }


@router.post('/solve')
async def solve_matrix(data: InputData) -> list[list[str]]:
    """
    This endpoint returns the root path. You need to provide a list of rooms (regions).
    Each room is a dictionary where the keys are the coordinates of the room and the values 
    are empty string, "S" or "A".
    """
    try:
        solver = Solver(data.coordinates)
        return solver.solve()
    except InvalidInputError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except GurobiError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e


@router.get('/generate')
async def generate_matrix(num: int) -> list[dict[str, str]]:
    """
    This endpoint generates a random matrix of rooms. You need to provide the number of rooms.
    In response, you will get a list of rooms (regions).
    """
    try:
        data = generate_rooms(num)
        return data
    except InvalidInputError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except GurobiError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e
