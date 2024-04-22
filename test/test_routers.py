"""Test endpoints"""
import asyncio
import json
from test.test_solver import matrix_10x10_real_solution
from test.consts_input import input_matrix_10x10
import numpy as np
import pytest

from fastapi.testclient import TestClient
from httpx import AsyncClient

from main import app

# Create a test client using the TestClient class provided by FastAPI
test_client = TestClient(app=app)

hard_to_solve_example = {
    "coordinates": [
        {
            "14,9": "",
            "14,10": "",
            "14,11": "",
            "14,12": "",
            "14,13": "",
            "14,14": "",
            "14,15": "",
            "14,16": "",
            "14,17": "",
            "14,18": "",
            "14,19": "",
            "15,9": "",
            "15,10": "",
            "15,11": "",
            "15,12": "",
            "15,13": "",
            "15,14": "",
            "15,15": "",
            "15,16": "",
            "15,17": "",
            "15,18": "S",
            "15,19": "",
            "16,9": "",
            "16,10": "",
            "16,11": "",
            "16,12": "",
            "16,13": "",
            "16,14": "",
            "16,15": "",
            "16,16": "",
            "16,17": "",
            "16,18": "",
            "16,19": "",
            "17,9": "",
            "17,10": "",
            "17,11": "",
            "17,12": "",
            "17,13": "",
            "17,14": "",
            "17,15": "",
            "17,16": "",
            "17,17": "",
            "17,18": "",
            "17,19": "",
            "18,9": "",
            "18,10": "",
            "18,11": "",
            "18,12": "",
            "18,13": "",
            "18,14": "",
            "18,15": "",
            "18,16": "",
            "18,17": "",
            "18,18": "",
            "18,19": "",
            "19,9": "",
            "19,10": "",
            "19,11": "",
            "19,12": "",
            "19,13": "",
            "19,14": "",
            "19,15": ""
        },
        {
            "0,0": "",
            "0,1": "",
            "0,2": "",
            "0,3": "",
            "0,4": "",
            "0,5": "",
            "0,6": "",
            "0,7": "",
            "0,8": "",
            "0,9": "",
            "0,10": "",
            "0,11": "",
            "0,12": "",
            "0,13": "",
            "1,0": "",
            "1,1": "",
            "1,2": "",
            "1,3": "",
            "1,4": "",
            "1,5": "",
            "1,6": "",
            "1,7": "",
            "1,8": "",
            "1,9": ""
        },
        {
            "0,14": "",
            "0,15": "",
            "0,16": "",
            "0,17": "",
            "0,18": "",
            "0,19": "",
            "0,20": "",
            "0,21": "",
            "1,14": "",
            "1,15": "",
            "1,16": "",
            "1,17": "",
            "1,18": "",
            "1,19": "",
            "1,20": "",
            "1,21": "",
            "2,14": "",
            "2,15": "",
            "2,16": "",
            "2,17": "",
            "2,18": "",
            "2,19": "",
            "2,20": "",
            "2,21": "",
            "3,14": "",
            "3,15": "",
            "3,16": "",
            "3,17": "",
            "3,18": "",
            "3,19": "",
            "3,20": "S",
            "3,21": "",
            "4,14": "",
            "4,15": "",
            "4,16": "",
            "4,17": "",
            "4,18": "",
            "4,19": "",
            "4,20": "",
            "4,21": "",
            "5,14": "",
            "5,15": "",
            "5,16": "",
            "5,17": "",
            "5,18": "",
            "5,19": "",
            "5,20": "",
            "5,21": "",
            "6,14": "",
            "6,15": "",
            "6,16": "",
            "6,17": "",
            "6,18": "",
            "6,19": "",
            "6,20": "",
            "6,21": "",
            "7,14": "",
            "7,15": "",
            "7,16": "",
            "7,17": "",
            "7,18": "",
            "7,19": "",
            "7,20": "",
            "7,21": "",
            "8,14": "",
            "8,15": ""
        },
        {
            "1,10": "",
            "1,11": "",
            "1,12": "",
            "1,13": ""
        },
        {
            "2,0": "",
            "2,1": "",
            "2,2": "",
            "2,3": "",
            "2,4": "",
            "2,5": "",
            "2,6": "",
            "2,7": "",
            "2,8": "",
            "2,9": "",
            "2,10": "",
            "2,11": "",
            "2,12": "",
            "2,13": ""
        },
        {
            "3,0": "",
            "3,1": "",
            "4,0": "",
            "4,1": "",
            "5,0": "",
            "5,1": "",
            "6,0": "A",
            "6,1": "",
            "7,0": "",
            "7,1": "",
            "8,0": "",
            "8,1": "",
            "9,0": "",
            "9,1": "",
            "10,0": "",
            "10,1": "",
            "11,0": "",
            "11,1": "",
            "12,0": "",
            "12,1": "",
            "13,0": "",
            "13,1": "",
            "14,0": "",
            "14,1": "",
            "15,0": "",
            "15,1": "",
            "16,0": "",
            "16,1": "",
            "17,0": "",
            "17,1": "",
            "18,0": "",
            "18,1": "",
            "19,0": "",
            "19,1": "",
            "20,0": "",
            "20,1": "",
            "21,0": "",
            "21,1": ""
        },
        {
            "3,2": "",
            "3,3": "",
            "3,4": "",
            "3,5": "",
            "3,6": "",
            "3,7": "",
            "3,8": "",
            "3,9": "",
            "3,10": "",
            "3,11": "",
            "3,12": "",
            "3,13": ""
        },
        {
            "4,2": "",
            "4,3": "",
            "4,4": "",
            "4,5": "",
            "4,6": "",
            "4,7": "",
            "4,8": "",
            "4,9": "",
            "4,10": "",
            "4,11": "",
            "4,12": "",
            "4,13": "A"
        },
        {
            "5,2": "",
            "5,3": "",
            "5,4": "",
            "5,5": "",
            "5,6": "",
            "5,7": "",
            "5,8": "",
            "5,9": "",
            "6,2": "",
            "6,3": "A",
            "6,4": "",
            "6,5": "",
            "6,6": "",
            "6,7": "",
            "6,8": "",
            "6,9": "",
            "7,2": "",
            "7,3": "",
            "7,4": "",
            "7,5": "",
            "7,6": "",
            "7,7": "",
            "7,8": "",
            "7,9": "",
            "8,2": "",
            "8,3": "",
            "8,4": "",
            "8,5": "",
            "8,6": "",
            "8,7": "",
            "8,8": "",
            "8,9": "",
            "9,2": "",
            "9,3": "",
            "9,4": "",
            "9,5": "",
            "9,6": "",
            "9,7": "",
            "9,8": "",
            "9,9": "",
            "10,2": "",
            "10,3": "",
            "10,4": "",
            "10,5": "",
            "10,6": "",
            "10,7": "",
            "10,8": "",
            "10,9": "",
            "11,2": "",
            "11,3": "",
            "11,4": "",
            "11,5": "",
            "11,6": "",
            "11,7": "",
            "11,8": "",
            "11,9": "",
            "12,2": "",
            "12,3": "",
            "12,4": "",
            "12,5": "",
            "12,6": "",
            "12,7": "",
            "12,8": "",
            "12,9": "",
            "13,2": "",
            "13,3": "",
            "13,4": "",
            "13,5": "",
            "13,6": "",
            "13,7": "",
            "13,8": "",
            "13,9": "",
            "14,2": "",
            "14,3": "",
            "14,4": "",
            "14,5": "",
            "14,6": "",
            "14,7": "",
            "14,8": ""
        },
        {
            "5,10": "",
            "5,11": "",
            "5,12": "",
            "5,13": "S"
        },
        {
            "6,10": ""
        },
        {
            "6,11": "A",
            "6,12": "",
            "6,13": ""
        },
        {
            "7,10": "",
            "7,11": "",
            "7,12": "",
            "7,13": ""
        },
        {
            "8,10": "",
            "8,11": "",
            "8,12": "",
            "8,13": "A"
        },
        {
            "8,16": "",
            "8,17": "",
            "8,18": "",
            "8,19": "",
            "8,20": "",
            "8,21": "",
            "9,16": "",
            "9,17": "",
            "9,18": "",
            "9,19": "",
            "9,20": "",
            "9,21": "",
            "10,16": "",
            "10,17": "",
            "10,18": "",
            "10,19": "",
            "10,20": "",
            "10,21": "",
            "11,16": "",
            "11,17": "",
            "11,18": "",
            "11,19": "",
            "11,20": "",
            "11,21": "",
            "12,16": "",
            "12,17": "",
            "12,18": "",
            "12,19": "",
            "12,20": "",
            "12,21": "",
            "13,16": "",
            "13,17": "",
            "13,18": "",
            "13,19": "",
            "13,20": "",
            "13,21": ""
        },
        {
            "9,10": "",
            "9,11": "S",
            "9,12": "",
            "9,13": "",
            "9,14": "",
            "9,15": ""
        },
        {
            "10,10": "",
            "10,11": "",
            "10,12": "",
            "10,13": "",
            "10,14": ""
        },
        {
            "10,15": "A"
        },
        {
            "11,10": "",
            "11,11": "",
            "11,12": "",
            "11,13": "",
            "11,14": "S",
            "11,15": ""
        },
        {
            "12,10": "",
            "12,11": "",
            "12,12": "S",
            "12,13": "",
            "12,14": "",
            "12,15": "",
            "13,10": "",
            "13,11": "",
            "13,12": "",
            "13,13": "",
            "13,14": "",
            "13,15": ""
        },
        {
            "14,20": "S",
            "14,21": "",
            "15,20": ""
        },
        {
            "15,2": "",
            "15,3": "S",
            "15,4": "",
            "15,5": "",
            "15,6": "",
            "15,7": "",
            "15,8": ""
        },
        {
            "15,21": "",
            "16,21": "",
            "17,21": "",
            "18,21": "",
            "19,21": "",
            "20,21": "",
            "21,21": "S"
        },
        {
            "16,2": "",
            "16,3": "S",
            "16,4": "",
            "16,5": "",
            "16,6": "",
            "16,7": "",
            "16,8": ""
        },
        {
            "16,20": "A"
        },
        {
            "17,2": "",
            "17,3": "",
            "17,4": "",
            "17,5": "",
            "17,6": "",
            "17,7": "",
            "17,8": ""
        },
        {
            "17,20": "A"
        },
        {
            "18,2": "",
            "18,3": "",
            "18,4": "",
            "18,5": "",
            "19,2": "",
            "19,3": "",
            "19,4": "",
            "19,5": "",
            "20,2": "",
            "20,3": "",
            "20,4": "",
            "20,5": "",
            "21,2": "",
            "21,3": "",
            "21,4": "",
            "21,5": ""
        },
        {
            "18,6": "",
            "18,7": "A",
            "18,8": ""
        },
        {
            "18,20": "A"
        },
        {
            "19,6": "",
            "19,7": "S",
            "19,8": ""
        },
        {
            "19,16": "",
            "19,17": "",
            "19,18": "",
            "19,19": "",
            "19,20": "S"
        },
        {
            "20,6": "",
            "20,7": "",
            "20,8": "S"
        },
        {
            "20,9": "",
            "20,10": "",
            "20,11": "",
            "20,12": "",
            "20,13": "",
            "20,14": "",
            "21,9": "",
            "21,10": ""
        },
        {
            "20,15": "A",
            "20,16": ""
        },
        {
            "20,17": "",
            "20,18": "",
            "20,19": "",
            "20,20": "S"
        },
        {
            "21,6": "",
            "21,7": "",
            "21,8": ""
        },
        {
            "21,11": "",
            "21,12": "",
            "21,13": "S",
            "21,14": "",
            "21,15": ""
        },
        {
            "21,16": "S",
            "21,17": "",
            "21,18": "",
            "21,19": "",
            "21,20": ""
        }
    ]
}


def test_solve_matrix_valid_input():
    """Test for solving a matrix."""
    # Define valid input data
    valid_data = {"coordinates": input_matrix_10x10}

    # Send POST request to /solve endpoint with valid data
    response = test_client.post("/api/solve", json=valid_data)

    # Assert that the response status code is 200
    assert response.status_code == 200

    # Assert that the response contains the expected data (e.g., result of solving the matrix)
    solution_10x10 = np.array(response.json())
    assert np.array_equal(matrix_10x10_real_solution, solution_10x10)


def test_solve_matrix_invalid_input():
    """Test for solving a matrix with invalid input."""
    # Define invalid input data (e.g., missing coordinates)
    invalid_data = {"coordinates": []}

    # Send POST request to /solve endpoint with invalid data
    response = test_client.post("/api/solve", json=invalid_data)

    # Assert that the response status code is 400 (Bad Request)
    assert response.status_code == 400
    print("response.text", response.text)
    # Assert that the response contains the expected error message
    assert "The amount of rows and columns must be between 2 and 23" in response.text


def test_solve_matrix_hard_to_solve_for_gurobi_model():
    """Test for solving a matrix that exceeds the size limit of the Gurobi model."""
    response = test_client.post("/api/solve", json=hard_to_solve_example)

    # Assert that the response status code is 400 (Bad Request)
    assert response.status_code == 422
    print("response.text", response.text)
    # Assert that the response contains the expected error message
    # pylint: disable=C0301
    assert ("Model too large for size-limited license; visit https://gurobi.com/unrestricted for more inform"
            in response.text)


@pytest.mark.asyncio
async def test_generate_rooms_valid_input(user_token):
    """Test for generating rooms with valid input."""
    # Define valid input data (e.g., number of rooms)
    valid_num = 5
    print("user_tokenuser_tokenuser_tokenuser_token", user_token)
    # Send GET request to /generate endpoint with valid input
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(
            f"/api/generate?num={valid_num}", headers={"Authorization": f"Bearer {user_token}"})

    # Assert that the response status code is 200
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_generate_rooms_invalid_input(user_token):
    """Test for generating rooms with invalid input."""
    # Define invalid input data (e.g., negative number of rooms)
    invalid_num = -1
    # Send GET request to /generate endpoint with invalid input

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(
            f"/api/generate?num={invalid_num}", headers={"Authorization": f"Bearer {user_token}"})

    # Assert that the response status code is 400 (Bad Request)
    assert response.status_code == 400
    # Assert that the response contains the expected error message
    assert "The amount of rows and columns must be between 2 and 23" in response.text


@pytest.mark.asyncio
async def test_get_condition_by_index():
    """Test for getting a condition by index."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.get("/api/generate-matrices-by-size?matrix_size=2&start=0&end=2")
        # we need to wait manually, as we didn't await when save to database
        # (for performance reasons)
        await asyncio.sleep(0.5)
        assert res.status_code == 200
        condition_res = await ac.get("/api/get-condition?matrix_size=2&index=1")
        assert condition_res.status_code == 200

    assert condition_res.status_code == 200
    expected_condition = '[{"0,1": ""}, {"0,0": "", "1,0": "", "1,1": ""}]'
    condition = json.loads(condition_res.json()['condition'])

    assert json.dumps(condition) == expected_condition


@pytest.mark.asyncio
async def test_document_not_found():
    """Test for getting a condition by index that does not exist."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.get("/api/generate-matrices-by-size?matrix_size=3&start=0&end=5")
        assert res.status_code == 200
        # we need to wait manually, as we didn't await when save to database
        # (for performance reasons)
        await asyncio.sleep(0.5)
        res = await ac.get("/api/get-condition?matrix_size=3&index=55")

    assert str(
        res.text) == '{"detail":"Document index out of range"}'


@pytest.mark.asyncio
async def test_collection_not_found():
    """Test for getting a condition by index when the collection does not exist."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.get("/api/get-condition?matrix_size=44&index=1")

    assert str(
        res.text) == '{"detail":"Document not found"}'


@pytest.mark.asyncio
async def test_matrix_2x2_full():
    """Test for getting a condition by index when the collection does not exist."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.get("/api/generate-matrices-by-size?matrix_size=2&symbols=SA")

    assert str(
        res.text) == "276"


@pytest.mark.asyncio
async def test_generate_user_conditions(user_token):
    """Test for getting conditions by user token."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(
            "/api/conditions", headers={"Authorization": f"Bearer {user_token}"})

    # Assert that the response status code is 200
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_not_found_conditions_for_user():
    """Test for getting conditions by user token when no conditions are found."""
    test_user = {"username": "conditions_not_found", "password": "123"}
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post(
            "/api/register-user",
            json=test_user,
        )
        res = await ac.post("/api/login", data=test_user, headers={
            "Content-Type": "application/x-www-form-urlencoded"})
        data = res.json()

        response = await ac.get(
            "/api/conditions", headers={"Authorization": f"Bearer {data['access_token']}"})

    assert response.text == '{"detail":"404: No matrices found for the specified user"}'
