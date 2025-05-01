from pydantic import BaseModel

class UserCreate(BaseModel):
    pseudo: str
    password: str

class UserLogin(BaseModel):
    pseudo: str
    password: str

class UserResponse(BaseModel):
    id: int
    pseudo: str

    class Config:
        orm_mode = True
