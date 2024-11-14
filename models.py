from pydantic import BaseModel

class Book(BaseModel):
    name: str
    author: str


class NewUser(BaseModel):
    username: str
    email: str
    password: str

class LoginUser(BaseModel):
    username : str
    password: str