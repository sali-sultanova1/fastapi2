from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    username: str
    password: str
    role: str ="user"
    createdAt: str | None = None

class PasswordUpdate(BaseModel):
    password: str