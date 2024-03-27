"""Endpoints for the solver module."""
from typing import List, Dict

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


class InputData(BaseModel):
    """Input data for the solver endpoint"""
    coordinates: List[Dict[str, str]]


@router.post('/solve')
async def solve_matrix(data: InputData):
    """
    This endpoint returns the root path.
    """
    try:
        solver = Solver(data.coordinates)
        return solver.solve()
    except InvalidInputError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except GurobiError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.get('/generate')
async def generate_matrix(num: int):
    """
    This endpoint generates a random matrix of rooms.
    """
    try:
        data = generate_rooms(num)
        return data
    except InvalidInputError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except GurobiError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
