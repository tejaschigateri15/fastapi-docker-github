from fastapi import FastAPI, Depends, status, Request, HTTPException, Path, Cookie, Response, Header
from cassandra_handler import CassandraDataPopulator
from models import Book, NewUser, LoginUser
from uuid import UUID
from typing import Annotated, Optional
import jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse

app = FastAPI()

cassandra_populator = None

SECRET_KEY = "b02325ad7c9b17d0c5ed13f80d45a91d6381661a83afd8eea31a7fc7fb9b1ee7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.on_event("startup")
async def startup_event():
    global cassandra_populator
    cassandra_populator = CassandraDataPopulator()
    print("Cassandra connection initialized")

@app.on_event("shutdown")
async def shutdown_event():
    if cassandra_populator:
        cassandra_populator.close()

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    print("hello   ",to_encode)
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("hello  ",payload)
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/")
def hello():
    return {"message": "hello world"}

@app.post('/user/register')
def register_user(new_user: NewUser):
    response = cassandra_populator.create_new_user(new_user)
    return response


@app.post('/user/login')
def login_user(login: LoginUser):
    response_data = cassandra_populator.verify_user(login)
    if response_data["status"] == "success":
        token = create_access_token({"sub": response_data["username"]})

        response = JSONResponse(
            content={"message": response_data["message"]},
            status_code=200
        )
        response.headers["Authorization"] = f"Bearer {token}"
        return response
    else:
        return response_data

@app.get("/books/")
def get_all_books(username:str = Depends(verify_token)):
    books = cassandra_populator.get_all_books()
    return {"books":books,"message": f"Hello {username}, here are your books"}



# books api


@app.post("/books/add", status_code=status.HTTP_200_OK)
async def add_book(book: Book):
    book_id = cassandra_populator.insert_book(book)
    return {"Book_id": str(book_id), "message": "Book added successfully"}




# get specific book

@app.get("/books/{id}")
def return_book(id: Annotated[str,Path(title="id",description="UUID of the book")]):
    try:
        uuid_id = UUID(id)
        books = cassandra_populator.ret_specific_book(uuid_id)
        if not books:
            return {"message": "Book not found"}
        return books
    except ValueError:
        return {"message": "Invalid UUID format"}

@app.get("/set-cookie/")
def set_cookie(response: Response):
    response.set_cookie(key="example_cookie", value="FastAPI_Cookie_Value")
    return {"message": "Cookie set successfully"}


@app.get("/read-cookie/")
def read_cookie(cookie_value: Optional[str] = Cookie(default=None)):
    return {"cookie_value": cookie_value}

