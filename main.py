from fastapi import FastAPI, status
from cassandra_handler import CassandraDataPopulator
from models import Book

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

@app.get("/")
def hello():
    return {"Hello": "world"}


@app.post("/books/add", status_code=status.HTTP_200_OK)
async def add_book(book: Book):
    book_id = cassandra_populator.insert_book(book)
    return {"Book_id": str(book_id), "message": "Book added successfully"}


@app.get("/books/")
def get_all_books():
    books = cassandra_populator.get_all_books()
    return books
