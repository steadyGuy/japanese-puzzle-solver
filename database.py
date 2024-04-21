"""Database module for MongoDB connection."""
import os
from motor.motor_asyncio import AsyncIOMotorClient

# MongoDB connection URL

mongo_root_username = os.getenv('MONGO_ROOT_USERNAME')
mongo_root_password = os.getenv('MONGO_ROOT_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')

MONGO_URL = f"mongodb://{mongo_root_username}:{mongo_root_password}@{db_host}:{db_port}/"
client = AsyncIOMotorClient(MONGO_URL)

DB = client[os.getenv('DB_NAME', 'main')]
