from typing import List
import configparser

import motor.motor_asyncio
from fastapi import APIRouter, Body, HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from ..models.item import ItemModel
from ..models.item import UpdateItemModel
from ..dependencies import get_token_header

config = configparser.ConfigParser()
config.read("config.ini")
client = motor.motor_asyncio.AsyncIOMotorClient(config["DEFAULT"]["mongo_uri"])
db = client.clothingDB
router = APIRouter(
    prefix="/item",
    tags=["item"],
    dependencies=[Depends(get_token_header)],
)


# Add a new item of clothing
@router.post("/", response_description="Add a new item", response_model=ItemModel)
async def add_item(item: ItemModel = Body(...)):
    item = jsonable_encoder(item)
    if await db["category"].find_one({"name": item["category"]}) is None:
        message = "Category {category} not found".format(category=item["category"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)
    new_item = await db["wardrobe"].insert_one(item)
    created_item = await db["wardrobe"].find_one({"_id": new_item.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_item)


# Get all items for a specific user
@router.get("/", response_description="List all items", response_model=List[ItemModel])
async def get_items():
    items = await db["wardrobe"].find().to_list(1000)
    return items


# Get one item by id
@router.get("/{_id}", response_description="Get a single item", response_model=ItemModel)
async def get_item(_id: str):
    if (item := await db["wardrobe"].find_one({"_id": _id})) is not None:
        return item
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item {_id} not found")


# Update an item by id
@router.put("/{_id}", response_description="Update an item", response_model=ItemModel)
async def update_item(_id: str, item: UpdateItemModel = Body(...)):
    item = {k: v for k, v in item.dict().items() if v is not None}

    if len(item) >= 1:
        update_result = await db["wardrobe"].update_one({"_id": _id}, {"$set": item})

        if update_result.modified_count == 1:
            if (updated_item := await db["wardrobe"].find_one({"_id": _id})) is not None:
                return updated_item

    if (existing_item := await db["wardrobe"].find_one({"_id": _id})) is not None:
        return existing_item

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item {_id} not found")


# Delete an item by id
@router.delete("/{_id}", response_description="Delete an item")
async def delete_item(_id: str):
    delete_result = await db["wardrobe"].delete_one({"_id": _id})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item {_id} not found")
