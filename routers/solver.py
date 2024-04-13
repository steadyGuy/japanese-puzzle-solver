"""Endpoints for the solver module."""
from fastapi import APIRouter, Depends, HTTPException
from gurobipy import GurobiError

from auth.utils import get_current_user
from database import DB
from solver.models import Condition
from solver.rooms_generator import generate_rooms
from solver.solver import Solver
from solver.utils import InvalidInputError

router = APIRouter(
    prefix='/api',
    tags=['solver']
)


@router.post('/solve')
async def solve_matrix(data: Condition) -> list[list[str]]:
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
async def generate_matrix(num: int, _: str = Depends(get_current_user)) -> list[dict[str, str]]:
    """
    This endpoint generates a random matrix of rooms. You need to provide the number of rooms.
    In response, you will get a list of rooms (regions).
    """
    try:
        data = generate_rooms(num)
        await DB["generated-rooms"].insert_one({"coordinates": data})
        return data
    except InvalidInputError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except GurobiError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e
