from pydantic import BaseModel
from typing import Union
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from enum import Enum
import time
import json
from fastapi import FastAPI, Request, Depends, status, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware


from sqlalchemy.engine import Connection
from database import get_db
from models import UserCreate, UserResponse

app = FastAPI()

origins = [
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.middleware("http")
async def log_request_data(request: Request, call_next):
    method = request.method
    url = str(request.url)
    query_params = dict(request.query_params)

    # Untuk membaca body, kita perlu 'stream' ulang karena hanya bisa dibaca sekali
    body_bytes = await request.body()
    try:
        body = body_bytes.decode('utf-8')
        body_data = json.loads(body) if body else {}
    except Exception:
        body_data = body  # Bisa saja bukan JSON (misal: form)

    now = datetime.now()
    print("------ Incoming Request ------")
    print(f"Time       : {now}")
    print(f"Method     : {method}")
    print(f"URL        : {url}")
    print(f"Query      : {query_params}")
    print(f"Body       : {body_data}")
    print("-----------------------------")

    # Buat ulang request dengan body agar bisa diteruskan
    request = Request(request.scope, receive=lambda: {
                      'type': 'http.request', 'body': body_bytes})

    response = await call_next(request)
    return response
# class SimpleMiddleware(BaseHTTPMiddleware):
#     async def dispatch(self, request: Request, call_next):
#         # Sebelum request diproses
#         print("Middleware: Sebelum request")
#
#         response = await call_next(request)
#
#         # Setelah response dikembalikan
#         print("Middleware: Setelah request")
#         return response
#
#
# app.add_middleware(SimpleMiddleware)
#


items = {"foo": "The Foo Wrestlers"}
fake_items_db = [{"item_name": "Foo"}, {
    "item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/")
async def read_root():
    return {"Hello": "World"}


# @app.get("/items/")
# async def read_item(skip: int = 0, limit: int = 10):
#     return fake_items_db[skip: skip + limit]

@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": items[item_id]}


@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    print(item_dict)
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


# @app.get("/items/", status_code=201)
# async def read_items(q: str | None = None):
#     results = {}
#     if q:
#         results.update({"q": q})
#     return results
#
#
# @app.get("/items/")
# async def read_item(item_id: str, q: str | None = None, short: bool = False):
#     item = {"item_id": item_id}
#     if q:
#         item.update({"q": q})
#     if not short:
#         item.update(
#             {"description": "This is an amazing item that has a long description"}
#         )
#     return item
#

@app.get("/users")
async def read_users():
    return {"username": "jati"}


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
