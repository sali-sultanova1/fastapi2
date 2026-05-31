from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    username: str
    password: str
    role: str ="user"

class PasswordUpdate(BaseModel):
    password: str