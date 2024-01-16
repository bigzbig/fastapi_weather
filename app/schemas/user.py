from pydantic import BaseModel


class UserInpt(BaseModel):
    name: str
    email: str
    password: str


class UserOut(BaseModel):
    name: str
    email: str

    class Config:
        from_attributes = True
