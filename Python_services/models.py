from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from bson import ObjectId

from fastapi import FastAPI


# nosql/mongodb
class User(BaseModel):
    username: str
    password: str


class Photo(BaseModel):
    image: str


class UserInDB(User):
    _id: ObjectId
    role: str = "user"
    Email: str
    FirstName: str
    LastName: str
    DateOfBirth: str
    createdTime: datetime = Field(default_factory=datetime.utcnow)
    updatedTime: datetime = Field(default_factory=datetime.utcnow)


class TokenResponse(BaseModel):
    token: str
    userName: str
    firstName: str
    lastName: str
    type: str
    role: str


class TokenRequest(BaseModel):
    userName: str
    password: str
