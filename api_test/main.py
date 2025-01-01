from fastapi import FastAPI, Query
from typing import Annotated

app = FastAPI()

# @app.get("/")
# def read_root():
#     return{"message": "APIです"}

# @app.get("/items/{item_id}")
# def read_item(item_id):
#     return {"item_id": item_id, "item_name": "Tシャツ"}

items = ["Tシャツ", "スカート", "ブーツ", "コート"]

@app.get("/items")
def read_items(skip: int = 0, limit: Annotated[int, Query(ge=1,le=10)] = 10):
    return{"items": items[skip: skip+ limit]}