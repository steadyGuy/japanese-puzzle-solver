"""Entry point of the application."""

from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from database import DB

from routers import solver

app = FastAPI()

# Load .env file
load_dotenv()

print("Connected to MongoDB", DB)

# Configure CORS
app.add_middleware(
    # warning
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

app.include_router(solver.router, responses={
    400: {
        "description": "Bad Request",
        "content": {"application/json": {"example": {"detail": "Error message"}}},
    },
    422: {
        "description": "Un-processable Entity",
        "content": {"application/json": {"example": {"detail": "Error message"}}},
    },
}, )
