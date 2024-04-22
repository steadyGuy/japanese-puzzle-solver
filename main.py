"""Entry point of the application."""
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

import load_env  # pylint: disable=W0611
from routers import auth, solver

app = FastAPI()

# Configure CORS
app.add_middleware(
    # warning
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

app.include_router(auth.router)
app.include_router(solver.router, responses={
    400: {
        "description": "Bad Request",
        "content": {"application/json": {"example": {"detail": "Error message"}}},
    },
    401: {
        "description": "Unauthorized",
        "content": {"application/json": {"example": {"detail": "Not authenticated"}}},
    },
    422: {
        "description": "Un-processable Entity",
        "content": {"application/json": {"example": {"detail": "Error message"}}},
    },
}, )
