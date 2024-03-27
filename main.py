"""Entry point of the application."""

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from routers import solver

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

app.include_router(solver.router)
