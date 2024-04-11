"""Models"""
from test.test_solver import input_matrix_7x7
from typing import Dict, List

from pydantic import BaseModel

example_data_for_docs: list = [
    {
        "coordinates": input_matrix_7x7
    }
]


class Condition(BaseModel):
    """Input data for the solver endpoint"""
    coordinates: List[Dict[str, str]]

    model_config = {
        "json_schema_extra": {
            "examples": example_data_for_docs,
        }
    }
