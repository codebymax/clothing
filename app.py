from typing import List

import motor.motor_asyncio
from fastapi import FastAPI, Body, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from models import ItemModel
from models import UpdateItemModel

uri = "mongodb+srv://rootUser:iowastatemongo@main-xz1r5.mongodb.net/clothingDB?retryWrites=true&w=majority"
client = motor.motor_asyncio.AsyncIOMotorClient(uri)
db = client.clothingDB
app = FastAPI()


@app.post("/", response_description="Add a new item", response_model=ItemModel)
async def add_item(item: ItemModel = Body(...)):
    item = jsonable_encoder(item)
    new_item = await db["wardrobe"].insert_one(item)
    created_item = await db["wardrobe"].find_one({"_id": new_item.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_item)


@app.get("/", response_description="List all items", response_model=List[ItemModel])
async def get_items():
    items = await db["wardrobe"].find().to_list(1000)
    return items


@app.get("/{id}", response_description="Get a single item", response_model=ItemModel)
async def get_item(id: str):
    if (item := await db["wardrobe"].find_one({"_id": id})) is not None:
        return item
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item {id} not found")


@app.put("/{id}", response_description="Update an item", response_model=ItemModel)
async def update_item(id: str, item: UpdateItemModel = Body(...)):
    item = {k: v for k, v in item.dict().items() if v is not None}

    if len(item) >= 1:
        update_result = await db["wardrobe"].update_one({"_id": id}, {"$set": item})

        if update_result.modified_count == 1:
            if (updated_item := await db["wardrobe"].find_one({"_id": id})) is not None:
                return updated_item

    if (existing_item := await db["wardrobe"].find_one({"_id": id})) is not None:
        return existing_item

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item {id} not found")


@app.delete("/{id}", response_description="Delete an item")
async def delete_item(id: str):
    delete_result = await db["wardrobe"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item {id} not found")
