from typing import List

from fastapi import APIRouter, Body, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from ..models.outfit import OutfitModel
from ..models.outfit import UpdateOutfitModel
from ..utils import db

router = APIRouter(
    prefix="/outfit",
    tags=["outfit"],
)


@router.post("/", response_description="Add a new outfit", response_model=OutfitModel)
async def add_outfit(outfit: OutfitModel = Body(...)):
    outfit = jsonable_encoder(outfit)
    new_outfit = await db["outfit"].insert_one(outfit)
    created_outfit = await db["outfit"].find_one({"_id": new_outfit.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_outfit)


@router.get("/", response_description="List all outfits", response_model=List[OutfitModel])
async def get_outfits():
    outfits = await db["outfit"].find().to_list(1000)
    return outfits


@router.get("/{id}", response_description="Get a single outfit", response_model=OutfitModel)
async def get_item(_id: str):
    if (outfit := await db["outfit"].find_one({"_id": _id})) is not None:
        return outfit
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Outfit {_id} not found")


@router.put("/{id}", response_description="Update an outfit", response_model=OutfitModel)
async def update_item(_id: str, item: UpdateOutfitModel = Body(...)):
    outfit = {k: v for k, v in item.dict().items() if v is not None}

    if len(outfit) >= 1:
        update_result = await db["outfit"].update_one({"_id": _id}, {"$set": outfit})

        if update_result.modified_count == 1:
            if (updated_item := await db["outfit"].find_one({"_id": _id})) is not None:
                return updated_item

    if (existing_item := await db["outfit"].find_one({"_id": _id})) is not None:
        return existing_item

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Outfit {_id} not found")


@router.delete("/{id}", response_description="Delete an outfit")
async def delete_item(_id: str):
    delete_result = await db["outfit"].delete_one({"_id": _id})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Outfit {_id} not found")