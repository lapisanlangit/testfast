

from fastapi import APIRouter, Depends, HTTPException
from models.item_model import ItemCreate, ItemResponse

from models.response_model import ResponseModel
from controllers.item_controller import (
    get_all_items,
    create_item,
    get_item_by_id,
    delete_item,
)

router = APIRouter()


@router.get("/", response_model=ResponseModel)
async def read_items():
    return await get_all_items()


@router.post("/", response_model=ResponseModel)
async def add_item(item: ItemCreate):
    return await create_item(item)


@router.get("/{item_id}", response_model=ResponseModel)
async def read_item(item_id: int):
    return await get_item_by_id(item_id)


@router.delete("/{item_id}", response_model=ResponseModel)
async def remove_item(item_id: int):
    return await delete_item(item_id)
