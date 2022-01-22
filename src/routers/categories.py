from typing import List
import configparser

import motor.motor_asyncio
from fastapi import APIRouter, Body, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from ..models.category import CategoryModel
from ..models.category import UpdateCategoryModel

config = configparser.ConfigParser()
config.read("config.ini")
client = motor.motor_asyncio.AsyncIOMotorClient(config["DEFAULT"]["mongo_uri"])
db = client.clothingDB
router = APIRouter(
    prefix="/category",
    tags=["category"],
)


# Add a new category
@router.post("/", response_description="Add a new category", response_model=CategoryModel)
async def add_item(category: CategoryModel = Body(...)):
    category = jsonable_encoder(category)
    new_category = await db["category"].insert_one(category)
    created_category = await db["category"].find_one({"_id": new_category.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_category)


# Get all categories
@router.get("/", response_description="List all categories", response_model=List[CategoryModel])
async def get_items():
    categories = await db["category"].find().to_list(1000)
    return categories


# Get one category by id
@router.get("/{_id}", response_description="Get a single category", response_model=CategoryModel)
async def get_item(_id: str):
    if (category := await db["category"].find_one({"_id": _id})) is not None:
        return category
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Category {id} not found")


# Update a category by id
@router.put("/{_id}", response_description="Update a category", response_model=CategoryModel)
async def update_item(_id: str, category: UpdateCategoryModel = Body(...)):
    category = {k: v for k, v in category.dict().items() if v is not None}

    if len(category) >= 1:
        update_result = await db["category"].update_one({"_id": _id}, {"$set": category})

        if update_result.modified_count == 1:
            if (updated_category := await db["category"].find_one({"_id": _id})) is not None:
                return updated_category

    if (existing_category := await db["category"].find_one({"_id": _id})) is not None:
        return existing_category

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Category {_id} not found")


# Delete a category by id
@router.delete("/{_id}", response_description="Delete an item")
async def delete_item(_id: str):
    delete_result = await db["category"].delete_one({"_id": _id})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item {_id} not found")