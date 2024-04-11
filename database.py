"""Database module for MongoDB connection."""
import os
from motor.motor_asyncio import AsyncIOMotorClient

# MongoDB connection URL
MONGO_URL = f"mongodb://{os.getenv('MONGO_ROOT_USERNAME')}:{os.getenv(
    'MONGO_ROOT_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/"
client = AsyncIOMotorClient(MONGO_URL)

DB = client[os.getenv('DB_NAME', 'main')]
