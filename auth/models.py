"""Models for auth process."""
from pydantic import BaseModel


class User(BaseModel):
    """User model"""
    username: str | None = None
    hashed_password: str


class Token(BaseModel):
    """Token model"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Token data model"""
    username: str


class UserLogin(BaseModel):
    """User login model"""
    username: str
    password: str
