from fastapi import FastAPI, status,Request
from cassandra_handler import CassandraDataPopulator
from models import Book
from uuid import  UUID

app = FastAPI()

cassandra_populator = None

@app.on_event("startup")
async def startup_event():
    global cassandra_populator
    cassandra_populator = CassandraDataPopulator()
    print("Cassandra connection initialized")

@app.on_event("shutdown")
async def shutdown_event():
    if cassandra_populator:
        cassandra_populator.close()

@app.middleware("http")
async def simple_middleware(request: Request, call_next):
    print(f"Incoming request: {request.method} {request.url.path}")
    response = await call_next(request)
    print(f"Outgoing response: Status Code {response.status_code}")
    return response

@app.get("/")
def hello():
    return {"message": "hello world"}


@app.post("/books/add", status_code=status.HTTP_200_OK)
async def add_book(book: Book):
    book_id = cassandra_populator.insert_book(book)
    return {"Book_id": str(book_id), "message": "Book added successfully"}


@app.get("/books/")
def get_all_books():
    books = cassandra_populator.get_all_books()
    return books

# get specific book

@app.get("/books/{id}")
def return_book(id: str):
    try:
        uuid_id = UUID(id)
        books = cassandra_populator.ret_specific_book(uuid_id)
        if not books:
            return {"message": "Book not found"}
        return books

    except ValueError:
        return {"message": "Invalid UUID format"}
