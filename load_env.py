"""Loads environment variables from .env-based files."""
import os

from dotenv import load_dotenv

load_dotenv('.env' if os.getenv('ENV') != 'test' else '.env.test')
