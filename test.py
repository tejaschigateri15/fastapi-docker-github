from fastapi import FastAPI,Query,Body
from typing import Annotated
from pydantic import BaseModel

app = FastAPI()

# class Item(BaseModel):
#     name : str
#     price: int
#     description: str | None = None



@app.get("/")
def hello() -> dict:
    return {"message": "hello world"}

@app.get("/test")
def test(id: int = 0) -> dict:
    return {"id": id}

# @app.get("/items/{item_id}")
# async def read_item(item_id: str, q: str | None = None):
#     if q:
#         return {"item_id": item_id, "q": q}
#     return {"item_id": item_id}



# @app.get("/items")
# def read_items(q: Annotated[str | None, Query(max_length=50)] = None):
#     print(q)
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results

# @app.get("/items/")
# async def read_items(q: Annotated[list[str] | None, Query()] = None):
#     query_items = {"q": q}
#     return query_items
#
# @app.post("/items")
# async def post_item(item:Item):
#     return item
#
# @app.put("/items/{items_id}")
# def function(items_id:int,item:Annotated[Item,Body(embed=True)]):
#     results = {"item_id": items_id, "item": item}
#     return results

class Image(BaseModel):
    url: str
    name: str


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    image: Image | None = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results


