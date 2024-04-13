"""Endpoints for the solver module."""
from fastapi import APIRouter, Depends, HTTPException
from gurobipy import GurobiError
from bson import json_util
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
async def generate_matrix(num: int, user: dict = Depends(get_current_user)) -> list[dict[str, str]]:
    """
    This endpoint generates a random matrix of rooms. You need to provide the number of rooms.
    In response, you will get a list of rooms (regions).
    """
    try:
        data = generate_rooms(num)

        await DB["generated-matrices"].insert_one({"coordinates": data, "user": user['id']})

        return data
    except InvalidInputError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except GurobiError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e


@router.get('/conditions')
async def get_conditions_by_user(user: dict = Depends(get_current_user)) -> list[dict[str, str]]:
    """Return a list of conditions by user id."""
    try:
        # Find documents with the specified user id
        conditions = await DB['generated-matrices'].find({"user": user['id']}).to_list(length=None)

        if conditions:
            return [
                {
                    "id": str(doc["_id"]),
                    "coordinates": json_util.dumps(doc["coordinates"])
                }
                for doc in conditions
            ]
        else:
            raise HTTPException(
                status_code=404, detail="No matrices found for the specified user")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
